from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')

# Use DATABASE_URL if the host provides it; otherwise use local sqlite.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///health_platform.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------- Models ----------
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    youtube_id = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    slug = db.Column(db.String(300), nullable=False, unique=True)
    summary = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(120), default="Health Team")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    steps = db.Column(db.Text, nullable=True)
    picture_url = db.Column(db.String(255), nullable=True)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    sleep_hours = db.Column(db.Float)
    activity_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, default=date.today)
    mood_score = db.Column(db.Integer)
    note = db.Column(db.Text)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    doctor = db.Column(db.String(120), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- DB init & seed ----------
def seed_data():
    if not Video.query.first():
        vids = [
            Video(title="Staying Mentally Healthy", youtube_id="oHg5SJYRHA0", description="Practical tips for mental well-being."),
            Video(title="10-Minute Home Workout", youtube_id="UItWltVZZmE", description="Quick routine to keep active."),
            Video(title="Mindfulness for Beginners", youtube_id="SEfs5TJZ6Nk", description="Intro to mindfulness & breathing."),
        ]
        db.session.add_all(vids)

    if not Article.query.first():
        arts = [
            Article(
                title="Sleep Hygiene: Practical Tips for Better Sleep",
                slug="sleep-hygiene-tips",
                summary="Good sleep supports memory, immunity and emotional balance.",
                content="<h3>Why sleep matters</h3><p>Sleep helps consolidate memory and repair the body.</p>"
            )
        ]
        db.session.add_all(arts)

    if not Recipe.query.first():
        recipes = [
            Recipe(name="Sukuma Wiki and Ugali", summary="A nutrient-dense Kenyan staple. Sukuma Wiki (collard greens) is packed with vitamins A, C, and K, while Ugali provides sustained energy from complex carbohydrates. This is a low-fat and high-fiber meal.", steps="1. For Ugali, bring water to a boil, then slowly stir in maize flour until a firm dough forms. 2. For Sukuma Wiki, heat oil in a pan, add finely chopped onions and garlic. 3. Add the chopped greens and cook until wilted. Season with salt and pepper. 4. Serve the fiber-rich greens alongside a serving of Ugali.", picture_url="/static/images/recipe1.webp"),
            Recipe(name="Githeri (Maize and Beans)", summary="A wholesome, high-protein vegetarian dish. This one-pot meal is an excellent source of plant-based protein, dietary fiber, and essential minerals, which help promote good digestion and heart health.", steps="1. Sauté onions, garlic, and ginger in a pot. Add chopped tomatoes and cook until they form a thick paste. 2. Stir in pre-boiled maize and beans, then add chopped potatoes and carrots. 3. Add a little water, cover, and simmer until the vegetables are tender.", picture_url="/static/images/recipe2.jpg"),
            Recipe(name="Kenyan Mahamri", summary="These light, cardamom-spiced pastries are a healthier breakfast option when baked or cooked with less oil. They are a source of carbohydrates for energy and can be served with a high-protein side like beans or eggs.", steps="1. In a bowl, mix flour, sugar, cardamom, and yeast. Add warm coconut milk and knead until a soft dough forms. 2. Let the dough rise for an hour. 3. Roll out the dough, cut into triangles, and shallow fry in healthy oil or bake until golden brown.", picture_url="/static/images/recipe3.jpg"),
            Recipe(name="Kaimati (Sweet Dumplings)", summary="A delightful treat for special occasions. These dumplings provide a quick source of energy. To make them healthier, use whole wheat flour and a minimal amount of natural sweetener like honey.", steps="1. Mix flour, yeast, salt, and sugar with water to form a thick batter. Let it rise. 2. Drop small spoonfuls of the batter into hot oil and fry until golden. 3. Drizzle the fried dumplings with a minimal amount of honey or a light sugar syrup.", picture_url="/static/images/recipe4.jpg"),
            Recipe(name="Mukimo", summary="A hearty and fiber-rich dish. The combination of potatoes, maize, and beans offers a balanced mix of carbohydrates, protein, and fiber, making it a highly satisfying and nutritious meal.", steps="1. Boil potatoes, maize, beans, and pumpkin leaves or spinach until soft. 2. Mash the mixture, gradually adding a little reserved water. 3. Season with salt and add some finely chopped spring onions.", picture_url="/static/images/recipe5.jpeg"),
            Recipe(name="Pilau", summary="A fragrant, flavorful, and healthy rice dish. Pilau is a source of complex carbohydrates and can be made with lean proteins like chicken or vegetables for a well-rounded meal. The spices used are known for their antioxidant properties.", steps="1. Sauté onions in a pot until caramelized. Add garlic and ginger paste, then stir in Pilau spice mix. 2. Add lean meat or vegetables and brown them. 3. Stir in basmati rice, then add hot water or broth. Cook until the water is absorbed.", picture_url="/static/images/recipe6.jpg"),
            Recipe(name="Matoke (Green Banana Stew)", summary="This comforting stew is an excellent source of potassium and other minerals from the green bananas. When prepared with a variety of vegetables and a light tomato base, it's a very low-fat, high-fiber meal.", steps="1. Sauté onions and garlic in a pot. Add chopped tomatoes and cook until they break down. 2. Add peeled and chopped green bananas, potatoes, and carrots. 3. Pour in broth and simmer until the bananas are tender and the stew has thickened.", picture_url="/static/images/recipe7.jpg"),
            Recipe(name="Kenyan Chicken Curry", summary="A lean and flavorful curry. Made with skinless chicken breast and cooked in a light coconut milk sauce, this dish is a fantastic source of protein. The spices add a flavorful punch without the need for excessive fat.", steps="1. Sauté onions, garlic, and ginger until soft. Add curry powder and cook for a minute. 2. Add chicken pieces and brown them. 3. Stir in chopped tomatoes, then coconut milk. Simmer until the chicken is cooked through.", picture_url="/static/images/recipe8.jpg"),
            Recipe(name="Kachumbari Salad", summary="A simple, refreshing, and highly nutritious salad. This is a powerful antioxidant booster with vitamins from the tomatoes and onions. The chili adds a metabolism-boosting kick, while the lime juice provides a healthy dose of vitamin C.", steps="1. Finely dice tomatoes, red onions, and a green chili (optional). 2. Place all the chopped ingredients in a bowl. 3. Squeeze fresh lime juice over the salad and toss gently to combine. 4. Serve immediately.", picture_url="/static/images/recipe9.jpg"),
            Recipe(name="Avocado Salad", summary="A light, high-fat, and nutrient-dense salad. Avocados are rich in healthy monounsaturated fats, which are great for heart health. This salad is also a good source of fiber and vitamins from the fresh vegetables.", steps="1. Chop ripe avocados and cherry tomatoes into bite-sized pieces. 2. In a small bowl, whisk together the juice of one lemon, a tablespoon of olive oil, salt, and black pepper. 3. Gently combine the chopped avocado and tomatoes in a large bowl. 4. Pour the dressing over the salad and toss to coat. 5. Serve immediately.", picture_url="/static/images/recipe10.jpg"),
        ]
        db.session.add_all(recipes)

    db.session.commit()

def create_and_seed():
    # do not drop existing tables (keeps data safe in production)
    db.create_all()
    seed_data()

# ---------- Routes ----------
@app.route('/')
def index():
    videos = Video.query.order_by(Video.created_at.desc()).limit(6).all()
    articles = Article.query.order_by(Article.created_at.desc()).limit(3).all()
    recipes = Recipe.query.order_by(Recipe.id.desc()).limit(3).all()
    return render_template('index.html', videos=videos, articles=articles, recipes=recipes)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')
# Add this near your other imports
from flask import jsonify

# ----------------------------
# API route for videos
# ----------------------------
@app.route('/api/videos')
def get_videos():
    videos = [
        {
            "title": "10 Minute Morning Yoga",
            "youtube_id": "abcd1234",
            "description": "Start your day with energy using this short yoga session."
        },
        {
            "title": "Healthy Eating Tips",
            "youtube_id": "efgh5678",
            "description": "Learn how to maintain a balanced diet for better health."
        },
        {
            "title": "Mental Health Awareness",
            "youtube_id": "ijkl9101",
            "description": "Understanding the importance of mental well-being."
        }
    ]
    return jsonify(videos)


@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/recipes')
def recipes():
    return render_template('recipes.html')

@app.route('/ask_doctor')
def ask_doctor():
    return render_template('ask_doctor.html')

@app.route('/appointments')
def appointments():
    all_appointments = Appointment.query.order_by(Appointment.appointment_date.asc()).all()
    now = datetime.now()
    return render_template('appointments.html', appointments=all_appointments, now=now)

@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        doctor = request.form.get('doctor')
        appointment_date = request.form.get('appointment_date')
        notes = request.form.get('notes')

        if not name or not email or not doctor or not appointment_date:
            flash("All required fields must be filled!", "danger")
            return redirect(url_for('book_appointment'))

        try:
            appointment_dt = datetime.strptime(appointment_date, "%Y-%m-%d %H:%M")
        except ValueError:
            flash("Invalid date format! Use YYYY-MM-DD HH:MM", "danger")
            return redirect(url_for('book_appointment'))

        new_appointment = Appointment(
            name=name,
            email=email,
            doctor=doctor,
            appointment_date=appointment_dt,
            notes=notes
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash("Appointment booked successfully!", "success")
        return redirect(url_for('appointments'))

    return render_template('book_appointment.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    profile_data = Profile.query.first()
    if request.method == 'POST':
        if not profile_data:
            profile_data = Profile()
            db.session.add(profile_data)
        profile_data.display_name = request.form.get('display_name')
        profile_data.age = request.form.get('age', type=int)
        profile_data.gender = request.form.get('gender')
        profile_data.sleep_hours = request.form.get('sleep_hours', type=float)
        profile_data.activity_minutes = request.form.get('activity_minutes', type=int)
        profile_data.notes = request.form.get('notes')
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile'))
    return render_template('profile.html', profile=profile_data)

@app.route('/mood_tracker', methods=['GET', 'POST'])
def mood_tracker():
    if request.method == 'POST':
        score = request.form.get('mood_score', type=int)
        note = request.form.get('note', '')
        if score:
            entry = MoodEntry(entry_date=date.today(), mood_score=score, note=note)
            db.session.add(entry)
            db.session.commit()
            flash("Mood entry saved successfully!", "success")
        return redirect(url_for('mood_tracker'))

    entries = MoodEntry.query.order_by(MoodEntry.entry_date.desc()).all()
    return render_template('mood_tracker.html', entries=entries)

@app.route('/self_assessment')
def self_assessment():
    return render_template('self_assessment.html')

@app.route('/goals')
def goals():
    return render_template('goals.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/dashboard')
def dashboard():
    profile_data = Profile.query.first()
    mood_entries = MoodEntry.query.order_by(MoodEntry.entry_date.desc()).all()
    suggestions = [
        {'title': 'Stay Hydrated', 'desc': 'Drink at least 8 cups of water daily.'},
        {'title': 'Daily Walk', 'desc': 'Walk 30 minutes every day for better health.'}
    ]
    return render_template('dashboard.html', profile=profile_data, mood_entries=mood_entries, suggestions=suggestions)

# ---------- API Routes ----------
@app.route('/api/mood_entries')
def api_mood_entries():
    entries = MoodEntry.query.order_by(MoodEntry.entry_date.asc()).all()
    data = [{'date': e.entry_date.strftime('%Y-%m-%d'), 'score': e.mood_score} for e in entries]
    return jsonify(data)

@app.route('/api/videos')
def api_videos():
    videos = Video.query.order_by(Video.created_at.desc()).all()
    video_list = [{
        'id': video.id,
        'title': video.title,
        'youtube_id': video.youtube_id,
        'description': video.description,
        'created_at': video.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for video in videos]
    return jsonify(video_list)

@app.route('/api/articles')
def api_articles():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    article_list = [{
        'id': article.id,
        'title': article.title,
        'slug': article.slug,
        'summary': article.summary,
        'created_at': article.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for article in articles]
    return jsonify(article_list)

@app.route('/api/recipes')
def api_recipes():
    recipes = Recipe.query.all()
    recipe_list = [{
        'id': recipe.id,
        'name': recipe.name,
        'summary': recipe.summary,
        'steps': recipe.steps,
        'picture_url': recipe.picture_url
    } for recipe in recipes]
    return jsonify(recipe_list)

# ---------- Run ----------
if __name__ == '__main__':
    with app.app_context():
        create_and_seed()
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)), debug=True)
