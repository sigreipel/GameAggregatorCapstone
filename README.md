## Game Recommendation Platform:
Django-based web application that aggregates and recommends video game news, updates, and developer information. It allows users to personalize their experience by following or blocking specific games or developers. The platform also includes a custom authentication system and a structured database design.

<ins>__Features:__</ins>
  Custom Authentication System
    
  - Using Django's `AbstractUser` and email as a login field.
  - Personalized user features (Following/Blocking games or developers)
    
  Game & Developer Database
  
  - Populated custom `placeholder_db.py` for script testing and UI prototyping.
  - Stores structured data on users, games, and developers.
    
  Game News Aggregation
  
  - Fetches and organizes data from multiple sources.
  - Filtering and displays relevant information based on user preferences.
    
  Scalable Backend
  
  - Built with Django, allowing SQLite for development.
  - Designed with other databases and cloud implementation in mind (AWS)
    
<ins>__TechStack:__</ins>

  Backend: Django (Python)
  
  Database: SQLite
  
  Frontend: Django templates, HTML, CSS
  
  Cloud Deployment: AWS (future integration)
    
<ins>__Future Improvements__</ins>
  
  - Full integration of real-time news API feeds
  - Advancing recommendations using filtering or ML personalization.
  - Deployment with Docker, Lambda, and AWS
