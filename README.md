# StreamView

StreamView is a web application that replicates YouTube’s user experience with a custom HTML and CSS frontend. Leveraging the YouTube Data API integrated via Django, StreamView allows users to search and retrieve videos seamlessly while providing a secure authentication system for personalized and protected access to content.

## Features

- **User-Friendly Interface**: Custom HTML and CSS designed to enhance the user experience, making it intuitive and easy to navigate.
- **Video Retrieval**: Integrated with the YouTube Data API for real-time video search and display based on user input.
- **Secure Authentication**: Robust authentication system ensuring user data and preferences are kept secure.
- **Personalized Experience**: Users can create accounts to save their favorite videos and access personalized content.
- **Responsive Design**: Works seamlessly on various devices and screen sizes.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django
- **APIs**: YouTube Data API
- **Database**: SQLite (or your chosen database)
- **Authentication**: Django Authentication System

## Installation

To get a local copy of StreamView up and running, follow these steps:

### Prerequisites

- Python 3.x
- Django
- pip (Python package manager)

# Clone the Repository and Install Dependencies

### 1. Clone the repository:
  - git clone https://github.com/yourusername/StreamView.git
  - cd StreamView
   
### 2. Install dependencies:
- pip install -r requirements.txt
- Configure Environment Variables
- Create a .env file in the root of the project.

### 3. Add your YouTube Data API key and any other necessary environment variables:
- YOUTUBE_API_KEY=your_youtube_api_key

### 4. Run Migrations
- python manage.py migrate

### 5. Start the Development Server
- python manage.py runserver
- Visit http://127.0.0.1:8000/ in your web browser to access StreamView.
