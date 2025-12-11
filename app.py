from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, date
import json
import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlencode

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID', '')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET', '')
STRAVA_REDIRECT_URI = os.getenv('STRAVA_REDIRECT_URI', 'http://localhost:8080/api/strava/callback')
STRAVA_AUTH_URL = 'https://www.strava.com/oauth/authorize'
STRAVA_TOKEN_URL = 'https://www.strava.com/oauth/token'
STRAVA_API_BASE = 'https://www.strava.com/api/v3'

# Try to import Firestore, fallback to local storage if not available
try:
    from google.cloud import firestore
    db = firestore.Client()
    USE_FIRESTORE = True
except Exception as e:
    print(f"Firestore not available, using local storage: {e}")
    USE_FIRESTORE = False
    LOCAL_DATA = {}

# Training plan data structure
TRAINING_PLAN = {
    "race_date": "2026-02-28",
    "goal": "Sub 1:50:00 (8:24/mile pace)",
    "race_name": "Wilmington Half Marathon",
    "weeks": [
        {
            "week_num": 1,
            "dates": "Dec 1-7",
            "total_miles": 27,
            "num_runs": 5,
            "phase": "BASE BUILDING",
            "workouts": [
                {"day": "Mon 12/1", "workout": "6 mi Easy (9:45-10:00)", "day_type": "DAY 1", "miles": 6},
                {"day": "Tue 12/2", "workout": "5 mi Easy + 4 strides", "day_type": "DAY 2", "miles": 5},
                {"day": "Wed 12/3", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Thu 12/4", "workout": "5 mi Easy", "day_type": "DAY 1", "miles": 5},
                {"day": "Fri 12/5", "workout": "5 mi Easy", "day_type": "DAY 2", "miles": 5},
                {"day": "Sat 12/6", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Sun 12/7", "workout": "6 mi Easy", "day_type": "DAY 1", "miles": 6}
            ]
        },
        {
            "week_num": 2,
            "dates": "Dec 8-14",
            "total_miles": 30,
            "num_runs": 5,
            "phase": "BASE BUILDING",
            "workouts": [
                {"day": "Mon 12/8", "workout": "5 mi Easy", "day_type": "DAY 2", "miles": 5},
                {"day": "Tue 12/9", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Wed 12/10", "workout": "6 mi Tempo (2 mi WU + 3 mi @ 8:05-8:15 + 1 mi CD)", "day_type": "DAY 1", "miles": 6},
                {"day": "Thu 12/11", "workout": "5 mi Easy + 4 strides", "day_type": "DAY 2", "miles": 5},
                {"day": "Fri 12/12", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Sat 12/13", "workout": "5 mi Easy", "day_type": "DAY 1", "miles": 5},
                {"day": "Sun 12/14", "workout": "9 mi Long Run Easy", "day_type": "DAY 2", "miles": 9}
            ]
        },
        {
            "week_num": 3,
            "dates": "Dec 15-21",
            "total_miles": 31,
            "num_runs": 4,
            "phase": "BASE BUILDING",
            "workouts": [
                {"day": "Mon 12/15", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Tue 12/16", "workout": "7 mi Easy", "day_type": "DAY 1", "miles": 7},
                {"day": "Wed 12/17", "workout": "7 mi Intervals (2 mi WU + 6x800m @ 7:30-7:40 w/ 400m jog + 1 mi CD)", "day_type": "DAY 2", "miles": 7},
                {"day": "Thu 12/18", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Fri 12/19", "workout": "7 mi Easy + 6 strides", "day_type": "DAY 1", "miles": 7},
                {"day": "Sat 12/20", "workout": "10 mi Long Run", "day_type": "DAY 2", "miles": 10},
                {"day": "Sun 12/21", "workout": "REST", "day_type": "DAY 3", "miles": 0}
            ]
        },
        {
            "week_num": 4,
            "dates": "Dec 22-28",
            "total_miles": 30,
            "num_runs": 5,
            "phase": "BASE BUILDING (RECOVERY)",
            "workouts": [
                {"day": "Mon 12/22", "workout": "6 mi Easy", "day_type": "DAY 1", "miles": 6},
                {"day": "Tue 12/23", "workout": "5 mi Easy", "day_type": "DAY 2", "miles": 5},
                {"day": "Wed 12/24", "workout": "REST (Christmas Eve)", "day_type": "DAY 3", "miles": 0},
                {"day": "Thu 12/25", "workout": "6 mi Easy + 4 strides (Christmas)", "day_type": "DAY 1", "miles": 6},
                {"day": "Fri 12/26", "workout": "3 mi Easy", "day_type": "DAY 2", "miles": 3},
                {"day": "Sat 12/27", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Sun 12/28", "workout": "10 mi Long Run Easy", "day_type": "DAY 1", "miles": 10}
            ]
        },
        {
            "week_num": 5,
            "dates": "Dec 29-Jan 4",
            "total_miles": 35,
            "num_runs": 5,
            "phase": "EARLY QUALITY",
            "workouts": [
                {"day": "Mon 12/29", "workout": "6 mi Easy", "day_type": "DAY 2", "miles": 6},
                {"day": "Tue 12/30", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Wed 12/31", "workout": "7 mi Tempo (2 mi WU + 4 mi @ 8:05-8:15 + 1 mi CD)", "day_type": "DAY 1", "miles": 7},
                {"day": "Thu 1/1", "workout": "5 mi Easy (New Year's Day)", "day_type": "DAY 2", "miles": 5},
                {"day": "Fri 1/2", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Sat 1/3", "workout": "6 mi Easy + 6 strides", "day_type": "DAY 1", "miles": 6},
                {"day": "Sun 1/4", "workout": "11 mi Long Run Easy", "day_type": "DAY 2", "miles": 11}
            ]
        },
        {
            "week_num": 6,
            "dates": "Jan 5-11",
            "total_miles": 35,
            "num_runs": 4,
            "phase": "EARLY QUALITY",
            "workouts": [
                {"day": "Mon 1/5", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Tue 1/6", "workout": "7 mi Easy + 6 strides", "day_type": "DAY 1", "miles": 7},
                {"day": "Wed 1/7", "workout": "8 mi Intervals (2 mi WU + 8x800m @ 7:30-7:40 w/ 400m jog + 2 mi CD)", "day_type": "DAY 2", "miles": 8},
                {"day": "Thu 1/8", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Fri 1/9", "workout": "7 mi Easy", "day_type": "DAY 1", "miles": 7},
                {"day": "Sat 1/10", "workout": "13 mi Long Run (10 mi easy + 3 mi @ 8:20-8:25)", "day_type": "DAY 2", "miles": 13},
                {"day": "Sun 1/11", "workout": "REST", "day_type": "DAY 3", "miles": 0}
            ]
        },
        {
            "week_num": 7,
            "dates": "Jan 12-18",
            "total_miles": 38,
            "num_runs": 5,
            "phase": "TRANSITION QUALITY",
            "workouts": [
                {"day": "Mon 1/12", "workout": "7 mi Easy", "day_type": "DAY 1", "miles": 7},
                {"day": "Tue 1/13", "workout": "6 mi Easy + 6 strides", "day_type": "DAY 2", "miles": 6},
                {"day": "Wed 1/14", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Thu 1/15", "workout": "7 mi Tempo (2 mi WU + 4 mi @ 8:05-8:15 + 1 mi CD)", "day_type": "DAY 1", "miles": 7},
                {"day": "Fri 1/16", "workout": "5 mi Recovery", "day_type": "DAY 2", "miles": 5},
                {"day": "Sat 1/17", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Sun 1/18", "workout": "13 mi Long Run (11 mi easy + 2 mi @ 8:20-8:25)", "day_type": "DAY 1", "miles": 13}
            ]
        },
        {
            "week_num": 8,
            "dates": "Jan 19-25",
            "total_miles": 40,
            "num_runs": 5,
            "phase": "TRANSITION QUALITY",
            "workouts": [
                {"day": "Mon 1/19", "workout": "7 mi Easy (MLK Day)", "day_type": "DAY 2", "miles": 7},
                {"day": "Tue 1/20", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Wed 1/21", "workout": "7 mi Tempo (2 mi WU + 4 mi @ 8:05-8:15 + 1 mi CD)", "day_type": "DAY 1", "miles": 7},
                {"day": "Thu 1/22", "workout": "5 mi Recovery", "day_type": "DAY 2", "miles": 5},
                {"day": "Fri 1/23", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Sat 1/24", "workout": "7 mi w/ 4x1 mi @ 8:20-8:25 (2 mi WU + intervals w/ 2 min rest + 1 mi CD)", "day_type": "DAY 1", "miles": 7},
                {"day": "Sun 1/25", "workout": "14 mi Long Run (12 mi easy + 2 mi @ 8:20-8:25)", "day_type": "DAY 2", "miles": 14}
            ]
        },
        {
            "week_num": 9,
            "dates": "Jan 26-Feb 1",
            "total_miles": 34,
            "num_runs": 4,
            "phase": "PEAK PHASE",
            "workouts": [
                {"day": "Mon 1/26", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Tue 1/27", "workout": "7 mi Easy + 6 strides", "day_type": "DAY 1", "miles": 7},
                {"day": "Wed 1/28", "workout": "7 mi Tempo (2 mi WU + 4 mi @ 8:05-8:15 + 1 mi CD)", "day_type": "DAY 2", "miles": 7},
                {"day": "Thu 1/29", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Fri 1/30", "workout": "6 mi Easy", "day_type": "DAY 1", "miles": 6},
                {"day": "Sat 1/31", "workout": "14 mi Long Run (10 mi easy + 4 mi @ 8:20-8:25)", "day_type": "DAY 2", "miles": 14},
                {"day": "Sun 2/1", "workout": "REST", "day_type": "DAY 3", "miles": 0}
            ]
        },
        {
            "week_num": 10,
            "dates": "Feb 2-8",
            "total_miles": 40,
            "num_runs": 5,
            "phase": "PEAK PHASE",
            "workouts": [
                {"day": "Mon 2/2", "workout": "6 mi Easy", "day_type": "DAY 1", "miles": 6},
                {"day": "Tue 2/3", "workout": "6 mi Easy + 4 strides", "day_type": "DAY 2", "miles": 6},
                {"day": "Wed 2/4", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Thu 2/5", "workout": "7 mi Tempo (2 mi WU + 4 mi @ 8:05-8:15 + 1 mi CD)", "day_type": "DAY 1", "miles": 7},
                {"day": "Fri 2/6", "workout": "5 mi Recovery", "day_type": "DAY 2", "miles": 5},
                {"day": "Sat 2/7", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Sun 2/8", "workout": "16 mi PEAK Long Run (12 mi easy + 4 mi @ 8:20-8:25 Goal Pace)", "day_type": "DAY 1", "miles": 16}
            ]
        },
        {
            "week_num": 11,
            "dates": "Feb 9-15",
            "total_miles": 34,
            "num_runs": 5,
            "phase": "RECOVERY & TRANSITION",
            "workouts": [
                {"day": "Mon 2/9", "workout": "6 mi Easy", "day_type": "DAY 2", "miles": 6},
                {"day": "Tue 2/10", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Wed 2/11", "workout": "6 mi Easy + 6 strides", "day_type": "DAY 1", "miles": 6},
                {"day": "Thu 2/12", "workout": "6 mi Tune-Up (2 mi WU + 3 mi @ 8:20-8:25 + 1 mi CD)", "day_type": "DAY 2", "miles": 6},
                {"day": "Fri 2/13", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Sat 2/14", "workout": "5 mi Easy (Valentine's Day)", "day_type": "DAY 1", "miles": 5},
                {"day": "Sun 2/15", "workout": "11 mi Long Run Easy (9:30-10:00)", "day_type": "DAY 2", "miles": 11}
            ]
        },
        {
            "week_num": 12,
            "dates": "Feb 16-22",
            "total_miles": 26,
            "num_runs": 5,
            "phase": "TAPER",
            "workouts": [
                {"day": "Mon 2/16", "workout": "REST (President's Day)", "day_type": "DAY 3", "miles": 0},
                {"day": "Tue 2/17", "workout": "5 mi Easy + 4 strides", "day_type": "DAY 1", "miles": 5},
                {"day": "Wed 2/18", "workout": "5 mi Easy", "day_type": "DAY 2", "miles": 5},
                {"day": "Thu 2/19", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Fri 2/20", "workout": "5 mi Sharpener (2 mi easy + 2x1 mi @ 8:20-8:25 w/ 2 min rest + 1 mi easy)", "day_type": "DAY 1", "miles": 5},
                {"day": "Sat 2/21", "workout": "8 mi Long Run Easy", "day_type": "DAY 2", "miles": 8},
                {"day": "Sun 2/22", "workout": "REST", "day_type": "DAY 3", "miles": 0}
            ]
        },
        {
            "week_num": 13,
            "dates": "Feb 23-28",
            "total_miles": 23.1,
            "num_runs": 4,
            "phase": "RACE WEEK",
            "workouts": [
                {"day": "Mon 2/23", "workout": "4 mi Easy", "day_type": "DAY 1", "miles": 4},
                {"day": "Tue 2/24", "workout": "3 mi Easy + 4 strides", "day_type": "DAY 2", "miles": 3},
                {"day": "Wed 2/25", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Thu 2/26", "workout": "3 mi Shakeout + 3 strides", "day_type": "DAY 1", "miles": 3},
                {"day": "Fri 2/27", "workout": "REST (complete rest before race)", "day_type": "DAY 2", "miles": 0},
                {"day": "Sat 2/28", "workout": "RACE DAY! 13.1 miles - WILMINGTON HALF MARATHON", "day_type": "RACE", "miles": 13.1},
                {"day": "Sun 3/1", "workout": "REST & CELEBRATE!", "day_type": "REST", "miles": 0}
            ]
        }
    ]
}

# File to store workout completions (fallback)
DATA_FILE = '/tmp/workout_data.json'

def load_workout_data():
    """Load saved workout completion data"""
    if USE_FIRESTORE:
        try:
            workouts_ref = db.collection('workouts')
            docs = workouts_ref.stream()
            data = {}
            for doc in docs:
                data[doc.id] = doc.to_dict()
            return data
        except Exception as e:
            print(f"Error loading from Firestore: {e}")
            return {}
    else:
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

def save_workout_data(key, data):
    """Save workout completion data"""
    if USE_FIRESTORE:
        try:
            db.collection('workouts').document(key).set(data)
            return True
        except Exception as e:
            print(f"Error saving to Firestore: {e}")
            return False
    else:
        all_data = load_workout_data()
        all_data[key] = data
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(all_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving to file: {e}")
            return False

@app.route('/')
def index():
    """Main page showing the full training plan"""
    # All data now fetched via API endpoints - no template variables needed
    return render_template('index.html')


@app.route('/api/log_workout', methods=['POST'])
def log_workout():
    """Log a workout as completed"""
    data = request.json
    week = data.get('week')
    day = data.get('day')
    completed = data.get('completed', False)
    notes = data.get('notes', '')
    actual_miles = data.get('actual_miles', '')
    actual_pace = data.get('actual_pace', '')
    duration = data.get('duration', '')
    strava_data = data.get('strava_data')
    
    key = f"w{week}_d{day}"
    
    # Check if this is effectively empty (no actual workout data)
    is_empty = (
        not actual_miles or 
        actual_miles.strip() == '' or 
        float(actual_miles) == 0
    ) and not notes.strip()
    
    # If empty, delete the workout record instead of saving
    if is_empty:
        if USE_FIRESTORE:
            try:
                db.collection('workouts').document(key).delete()
                return jsonify({'success': True, 'deleted': True, 'message': 'Workout data cleared'})
            except Exception as e:
                print(f"Error deleting workout: {e}")
                return jsonify({'success': False, 'error': 'Failed to delete workout'}), 500
        else:
            all_data = load_workout_data()
            if key in all_data:
                del all_data[key]
                try:
                    with open(DATA_FILE, 'w') as f:
                        json.dump(all_data, f, indent=2)
                    return jsonify({'success': True, 'deleted': True, 'message': 'Workout data cleared'})
                except Exception as e:
                    print(f"Error deleting workout: {e}")
                    return jsonify({'success': False, 'error': 'Failed to delete workout'}), 500
    
    # Load existing data to preserve edit information
    existing_data = load_workout_data()
    if key in existing_data:
        workout_info = existing_data[key]
    else:
        workout_info = {}
    
    # Update with logging data (preserves existing edit data)
    workout_info.update({
        'completed': completed,
        'notes': notes,
        'actual_miles': actual_miles,
        'actual_pace': actual_pace,
        'duration': duration,
        'date_logged': datetime.now().isoformat()
    })
    
    # Add Strava data if present
    if strava_data:
        workout_info['strava_data'] = strava_data
    
    success = save_workout_data(key, workout_info)
    
    if success:
        return jsonify({'success': True, 'data': workout_info})
    else:
        return jsonify({'success': False, 'error': 'Failed to save workout'}), 500

@app.route('/api/edit_workout', methods=['POST'])
def edit_workout():
    """Edit/modify a planned workout"""
    data = request.json
    week = data.get('week')
    day = data.get('day')
    
    # Original workout info
    original_workout = data.get('original_workout')
    original_miles = data.get('original_miles')
    
    # Modified workout info
    modified_workout = data.get('modified_workout')
    modified_miles = data.get('modified_miles')
    modified_type = data.get('modified_type')
    modification_reason = data.get('modification_reason', '')
    
    key = f"w{week}_d{day}"
    
    # Load existing data or create new
    existing_data = load_workout_data()
    if key not in existing_data:
        workout_info = {}
    else:
        workout_info = existing_data[key]
    
    # Update with modification
    workout_info.update({
        'is_modified': True,
        'original_workout': original_workout,
        'original_miles': original_miles,
        'modified_workout': modified_workout,
        'modified_miles': modified_miles,
        'modified_type': modified_type,
        'modification_reason': modification_reason,
        'modified_date': datetime.now().isoformat()
    })
    
    success = save_workout_data(key, workout_info)
    
    if success:
        return jsonify({'success': True, 'data': workout_info})
    else:
        return jsonify({'success': False, 'error': 'Failed to save modification'}), 500

@app.route('/api/revert_workout', methods=['POST'])
def revert_workout():
    """Revert a modified workout back to original"""
    data = request.json
    week = data.get('week')
    day = data.get('day')
    
    key = f"w{week}_d{day}"
    
    # Load existing data
    existing_data = load_workout_data()
    
    if key in existing_data:
        workout_info = existing_data[key]
        # Remove modification flags but keep completion status
        workout_info['is_modified'] = False
        workout_info.pop('modified_workout', None)
        workout_info.pop('modified_miles', None)
        workout_info.pop('modified_type', None)
        workout_info.pop('modification_reason', None)
        workout_info.pop('modified_date', None)
        
        success = save_workout_data(key, workout_info)
        
        if success:
            return jsonify({'success': True, 'data': workout_info})
        else:
            return jsonify({'success': False, 'error': 'Failed to revert'}), 500
    
    return jsonify({'success': False, 'error': 'Workout not found'}), 404

@app.route('/api/get_stats')
def get_stats():
    """Get training statistics"""
    workout_data = load_workout_data()
    
    total_workouts = sum(
        len([w for w in week['workouts'] if w['miles'] > 0])
        for week in TRAINING_PLAN['weeks']
    )
    
    completed_workouts = sum(
        1 for v in workout_data.values() if v.get('completed', False)
    )
    
    total_planned_miles = sum(week['total_miles'] for week in TRAINING_PLAN['weeks'])
    
    # Calculate total completed miles
    completed_miles = 0
    for key, value in workout_data.items():
        if value.get('completed', False):
            actual = value.get('actual_miles', '')
            if actual:
                try:
                    completed_miles += float(actual)
                except:
                    pass
    
    # Calculate weekly breakdown for chart
    weekly_actual_miles = [0] * 13
    for key, value in workout_data.items():
        if value.get('completed', False) and value.get('actual_miles'):
            try:
                # Parse key format: w1_d1 -> week 1
                week_num = int(key.split('_')[0][1:]) - 1  # w1 -> 0, w2 -> 1, etc.
                if 0 <= week_num < 13:
                    weekly_actual_miles[week_num] += float(value['actual_miles'])
            except (ValueError, IndexError):
                pass
    
    # Round weekly miles to 1 decimal place
    weekly_actual_miles = [round(miles, 1) for miles in weekly_actual_miles]
    
    return jsonify({
        'total_workouts': total_workouts,
        'completed_workouts': completed_workouts,
        'completion_percentage': round((completed_workouts / total_workouts * 100), 1) if total_workouts > 0 else 0,
        'total_planned_miles': total_planned_miles,
        'completed_miles': round(completed_miles, 1),
        'weekly_actual_miles': weekly_actual_miles  # NEW: Weekly breakdown for chart
    })

@app.route('/api/get_plan')
def get_plan():
    """Get the full training plan"""
    return jsonify(TRAINING_PLAN)

@app.route('/api/get_workouts')
def get_workouts():
    """Get all workout data from Firestore"""
    workout_data = load_workout_data()
    return jsonify(workout_data)

@app.route('/api/reset_plan', methods=['POST'])
def reset_plan():
    """Reset all workout data (for QA/testing)"""
    try:
        if USE_FIRESTORE:
            # Delete all documents in workouts collection
            workouts_ref = db.collection('workouts')
            docs = workouts_ref.stream()
            deleted_count = 0
            for doc in docs:
                doc.reference.delete()
                deleted_count += 1
            return jsonify({
                'success': True,
                'message': f'Reset complete! Deleted {deleted_count} logged workouts.',
                'deleted_count': deleted_count
            })
        else:
            # Clear local storage
            global LOCAL_DATA
            LOCAL_DATA = {}
            return jsonify({
                'success': True,
                'message': 'Reset complete! All data cleared.',
                'deleted_count': 0
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ============================================================================
# STRAVA INTEGRATION ENDPOINTS
# ============================================================================

def get_valid_strava_token():
    """Get valid Strava access token, refresh if needed"""
    try:
        if not USE_FIRESTORE:
            return None
            
        token_doc = db.collection('strava_tokens').document('user_token').get()
        
        if not token_doc.exists:
            return None
        
        token_data = token_doc.to_dict()
        
        # Check if token is expired (expires_at is Unix timestamp)
        if datetime.now().timestamp() >= token_data.get('expires_at', 0):
            # Token expired, refresh it
            print("Strava token expired, refreshing...")
            refresh_data = {
                'client_id': STRAVA_CLIENT_ID,
                'client_secret': STRAVA_CLIENT_SECRET,
                'grant_type': 'refresh_token',
                'refresh_token': token_data['refresh_token']
            }
            
            response = requests.post(STRAVA_TOKEN_URL, data=refresh_data)
            response.raise_for_status()
            new_tokens = response.json()
            
            # Update stored tokens
            db.collection('strava_tokens').document('user_token').update({
                'access_token': new_tokens['access_token'],
                'refresh_token': new_tokens['refresh_token'],
                'expires_at': new_tokens['expires_at'],
                'updated_at': datetime.now().isoformat()
            })
            
            print("Strava token refreshed successfully")
            return new_tokens['access_token']
        
        return token_data['access_token']
    
    except Exception as e:
        print(f"Error getting Strava token: {e}")
        return None

@app.route('/api/strava/authorize')
def strava_authorize():
    """Redirect user to Strava authorization page"""
    if not STRAVA_CLIENT_ID:
        return jsonify({'error': 'Strava not configured. Please set STRAVA_CLIENT_ID in environment.'}), 500
    
    params = {
        'client_id': STRAVA_CLIENT_ID,
        'redirect_uri': STRAVA_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'activity:read_all',
        'approval_prompt': 'auto'
    }
    auth_url = f"{STRAVA_AUTH_URL}?{urlencode(params)}"
    return jsonify({'auth_url': auth_url})

@app.route('/api/strava/callback')
def strava_callback():
    """Handle OAuth callback from Strava"""
    code = request.args.get('code')
    
    if not code:
        return '<html><body><h2>❌ Authorization failed</h2><p>No authorization code received.</p><button onclick="window.close()">Close</button></body></html>'
    
    try:
        # Exchange code for access token
        token_data = {
            'client_id': STRAVA_CLIENT_ID,
            'client_secret': STRAVA_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }
        
        response = requests.post(STRAVA_TOKEN_URL, data=token_data)
        response.raise_for_status()
        tokens = response.json()
        
        # Store tokens in Firestore
        if USE_FIRESTORE:
            db.collection('strava_tokens').document('user_token').set({
                'access_token': tokens['access_token'],
                'refresh_token': tokens['refresh_token'],
                'expires_at': tokens['expires_at'],
                'athlete_id': tokens['athlete']['id'],
                'athlete_name': f"{tokens['athlete']['firstname']} {tokens['athlete']['lastname']}",
                'updated_at': datetime.now().isoformat()
            })
        
        # Success page that closes popup
        return '''
        <html>
        <head><title>Strava Authorization</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h2>✅ Strava Connected Successfully!</h2>
            <p>You can close this window now.</p>
            <script>
                window.opener.postMessage({type: 'strava_auth_success'}, '*');
                setTimeout(() => window.close(), 2000);
            </script>
        </body>
        </html>
        '''
    
    except Exception as e:
        print(f"Error exchanging code for token: {e}")
        return f'<html><body><h2>❌ Authorization Error</h2><p>{str(e)}</p><button onclick="window.close()">Close</button></body></html>'

@app.route('/api/strava/check_auth')
def strava_check_auth():
    """Check if user has authorized Strava"""
    try:
        if not USE_FIRESTORE:
            return jsonify({'authorized': False, 'message': 'Firestore not available'})
        
        token_doc = db.collection('strava_tokens').document('user_token').get()
        if token_doc.exists:
            token_data = token_doc.to_dict()
            return jsonify({
                'authorized': True,
                'athlete_name': token_data.get('athlete_name', 'Unknown')
            })
        return jsonify({'authorized': False})
    except Exception as e:
        print(f"Error checking Strava auth: {e}")
        return jsonify({'authorized': False, 'error': str(e)})

@app.route('/api/strava/activities/<date>')
def get_strava_activities(date):
    """Get Strava activities for a specific date (YYYY-MM-DD)"""
    token = get_valid_strava_token()
    
    if not token:
        return jsonify({'error': 'Not authorized with Strava. Please connect your Strava account first.'}), 401
    
    try:
        # Parse date
        target_date = datetime.strptime(date, '%Y-%m-%d')
        
        # Get start and end of day (Unix timestamps)
        start_of_day = target_date.replace(hour=0, minute=0, second=0)
        end_of_day = target_date.replace(hour=23, minute=59, second=59)
        
        # Fetch activities from Strava
        headers = {'Authorization': f'Bearer {token}'}
        params = {
            'after': int(start_of_day.timestamp()),
            'before': int(end_of_day.timestamp()),
            'per_page': 20
        }
        
        response = requests.get(
            f'{STRAVA_API_BASE}/athlete/activities',
            headers=headers,
            params=params
        )
        response.raise_for_status()
        activities = response.json()
        
        # Filter to only runs
        runs = [a for a in activities if a['type'] in ['Run', 'VirtualRun']]
        
        # Format for frontend
        formatted_runs = []
        for run in runs:
            distance_miles = run['distance'] / 1609.34
            moving_time_seconds = run['moving_time']
            
            # Calculate pace
            if distance_miles > 0:
                pace_minutes_per_mile = (moving_time_seconds / 60) / distance_miles
                pace_min = int(pace_minutes_per_mile)
                pace_sec = int((pace_minutes_per_mile - pace_min) * 60)
                pace_str = f"{pace_min}:{pace_sec:02d} min/mi"
            else:
                pace_str = "N/A"
            
            # Format duration
            hours = moving_time_seconds // 3600
            minutes = (moving_time_seconds % 3600) // 60
            seconds = moving_time_seconds % 60
            if hours > 0:
                duration_str = f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                duration_str = f"{minutes}:{seconds:02d}"
            
            formatted_runs.append({
                'id': run['id'],
                'name': run['name'],
                'distance': round(distance_miles, 2),
                'duration': duration_str,
                'pace': pace_str,
                'moving_time': moving_time_seconds,
                'elapsed_time': run['elapsed_time'],
                'total_elevation_gain': round(run['total_elevation_gain'] * 3.28084, 0),
                'start_date': run['start_date'],
                'average_heartrate': run.get('average_heartrate'),
                'max_heartrate': run.get('max_heartrate')
            })
        
        return jsonify({'runs': formatted_runs, 'count': len(formatted_runs)})
    
    except Exception as e:
        print(f"Error fetching Strava activities: {e}")
        return jsonify({'error': f'Failed to fetch activities: {str(e)}'}), 500


if __name__ == '__main__':
    # For Google Cloud Run
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
