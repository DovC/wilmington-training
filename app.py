from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, date
import json
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

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
            "total_miles": 32,
            "num_runs": 5,
            "phase": "BASE BUILDING",
            "workouts": [
                {"day": "Mon 12/15", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Tue 12/16", "workout": "6 mi Easy", "day_type": "DAY 1", "miles": 6},
                {"day": "Wed 12/17", "workout": "7 mi Intervals (2 mi WU + 6x800m @ 7:30-7:40 w/ 400m jog + 1 mi CD)", "day_type": "DAY 2", "miles": 7},
                {"day": "Thu 12/18", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Fri 12/19", "workout": "6 mi Easy + 6 strides", "day_type": "DAY 1", "miles": 6},
                {"day": "Sat 12/20", "workout": "8 mi Long Run", "day_type": "DAY 2", "miles": 8},
                {"day": "Sun 12/21", "workout": "REST", "day_type": "DAY 3", "miles": 0}
            ]
        },
        {
            "week_num": 4,
            "dates": "Dec 22-28",
            "total_miles": 28,
            "num_runs": 5,
            "phase": "BASE BUILDING (RECOVERY)",
            "workouts": [
                {"day": "Mon 12/22", "workout": "6 mi Easy", "day_type": "DAY 1", "miles": 6},
                {"day": "Tue 12/23", "workout": "5 mi Easy", "day_type": "DAY 2", "miles": 5},
                {"day": "Wed 12/24", "workout": "REST (Christmas Eve)", "day_type": "DAY 3", "miles": 0},
                {"day": "Thu 12/25", "workout": "6 mi Easy + 4 strides (Christmas)", "day_type": "DAY 1", "miles": 6},
                {"day": "Fri 12/26", "workout": "3 mi Easy", "day_type": "DAY 2", "miles": 3},
                {"day": "Sat 12/27", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Sun 12/28", "workout": "8 mi Long Run Easy", "day_type": "DAY 1", "miles": 8}
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
            "total_miles": 36,
            "num_runs": 5,
            "phase": "EARLY QUALITY",
            "workouts": [
                {"day": "Mon 1/5", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Tue 1/6", "workout": "6 mi Easy + 6 strides", "day_type": "DAY 1", "miles": 6},
                {"day": "Wed 1/7", "workout": "7 mi Intervals (2 mi WU + 8x800m @ 7:30-7:40 w/ 400m jog + 1 mi CD)", "day_type": "DAY 2", "miles": 7},
                {"day": "Thu 1/8", "workout": "REST", "day_type": "DAY 3", "miles": 0},
                {"day": "Fri 1/9", "workout": "6 mi Easy", "day_type": "DAY 1", "miles": 6},
                {"day": "Sat 1/10", "workout": "12 mi Long Run (10 mi easy + 2 mi @ 8:20-8:25)", "day_type": "DAY 2", "miles": 12},
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
            "total_miles": 40,
            "num_runs": 5,
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
    workout_data = load_workout_data()
    return render_template('index.html', plan=TRAINING_PLAN, workout_data=workout_data)

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
    
    key = f"w{week}_d{day}"
    
    workout_info = {
        'completed': completed,
        'notes': notes,
        'actual_miles': actual_miles,
        'actual_pace': actual_pace,
        'date_logged': datetime.now().isoformat()
    }
    
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
    
    completed_miles = 0
    for key, value in workout_data.items():
        if value.get('completed', False):
            actual = value.get('actual_miles', '')
            if actual:
                try:
                    completed_miles += float(actual)
                except:
                    pass
    
    return jsonify({
        'total_workouts': total_workouts,
        'completed_workouts': completed_workouts,
        'completion_percentage': round((completed_workouts / total_workouts * 100), 1) if total_workouts > 0 else 0,
        'total_planned_miles': total_planned_miles,
        'completed_miles': round(completed_miles, 1)
    })

@app.route('/api/get_plan')
def get_plan():
    """Get the full training plan"""
    return jsonify(TRAINING_PLAN)

if __name__ == '__main__':
    # For Google Cloud Run
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
