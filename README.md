# MythLab – Explore, Learn and Discover

## 1. Project Overview

**MythLab** is a Python-based desktop application developed to help users explore myths, legends, mythical creatures and traditional stories from Bhutan and other cultures.

The application provides an interactive learning environment where users can read stories, discover mythical creatures, explore regional legends, test their knowledge through quizzes and manage personal learning tasks.

MythLab aims to make cultural stories more accessible and engaging by combining storytelling, images and interactive features in a single application.

The application was developed using Python, Tkinter and SQLite, with a dark-themed graphical user interface inspired by traditional storytelling and cultural heritage.

## 2. Project Objectives

The main objectives of MythLab are to:

- Provide an organised collection of myths, legends and mythical creatures.
- Introduce users to Bhutanese cultural stories and traditions.
- Allow users to search and explore stories by category.
- Present detailed stories with relevant images and descriptions.
- Help users explore myths associated with different regions of Bhutan.
- Encourage learning through interactive quizzes.
- Allow users to save favourite stories for future reading.
- Provide a task management feature to organise learning activities.
- Demonstrate the practical application of Python GUI programming and database management.

## 3. Main Features

### 3.1 User Registration and Login

MythLab provides registration and login functionality for users.

Users can create an account and log in to access the application and its personalised features.

### 3.2 Home Dashboard

The Home page serves as the main starting point of the application.

It provides an introduction to MythLab, featured stories and navigation options to access different sections.

### 3.3 Myths and Legends

The Myths section contains stories organised into different categories, including gods and goddesses, heroes, folklore and creatures.

Users can:

- Browse available myths.
- Search for specific stories.
- Filter stories by category.
- Open individual stories to read detailed information.
- Save stories to their favourites.

Examples include Guru Rinpoche, King Gesar, Drukpa Kunley and Ap Chhundu.

### 3.4 Mythical Creatures

The Creatures section introduces eight mythical creatures:

1. The Thunder Dragon
2. The Yeti
3. The Firebird
4. Migoi
5. Snow Lion
6. The Serpent King
7. The Giant Tortoise
8. Rangda

Each creature includes an image, a short description and a detailed story.

### 3.5 Regions of Bhutan

The Regions section allows users to explore Bhutanese myths and legends associated with different dzongkhags.

It includes a map of Bhutan and regional stories connected to places such as Paro, Thimphu, Punakha, Haa, Gasa and Trashigang.

### 3.6 Interactive Quiz

The Quiz section allows users to test their knowledge of myths, legends and mythical creatures.

Users can answer questions and view their results after completing a quiz.

### 3.7 My Tasks

The My Tasks section allows users to organise their learning activities.

Its main features include:

- Adding new tasks.
- Editing and deleting tasks.
- Marking tasks as completed.
- Searching and filtering tasks.
- Setting High, Medium or Low priority.
- Viewing task completion summaries.

### 3.8 Favourites

Users can save interesting myths and stories to their Favourites section for easier access later.

### 3.9 About

The About page provides information about MythLab, its purpose and its main features.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Tkinter | Graphical user interface |
| CustomTkinter | Rounded and modern interface components where used |
| SQLite | Local database storage |
| Pillow (PIL) | Loading and displaying images |
| Visual Studio Code | Code development and debugging |
| Git and GitHub | Version control and project sharing |

## 5. Project Structure

The project is organised into separate Python files to make the code easier to maintain.

```text
MythLab/
│
├── main.py
├── myths.py
├── myth_detail.py
├── creatures.py
├── region.py
├── quiz.py
├── task.py
├── favorites.py
├── about.py
├── assets/
├── mythlab.db
└── README.md
```

**Note:** Additional files may be present depending on the final project version. The SQLite database may be created during setup or included as an initial local database.

## 6. Installation and Setup

### Step 1: Install Python

Install Python 3 from the official website:

https://www.python.org/downloads/

During installation on Windows, select **Add Python to PATH**.

### Step 2: Download the Project

Download the MythLab project folder from the GitHub repository or obtain a copy of the project files.

Extract the ZIP file if necessary.

### Step 3: Open the Project

Open Visual Studio Code and select:

**File → Open Folder → MythLab**

### Step 4: Install Required Libraries

Open the VS Code terminal and run:

```bash
python -m pip install pillow customtkinter
```

Tkinter and SQLite are included with most standard Python installations.

### Step 5: Run the Application

Run the following command in the project directory:

```bash
python main.py
```

The MythLab application should open if all required files and dependencies are available.

## 7. How to Use MythLab

1. Launch the application using `python main.py`.
2. Register or log in using your account.
3. Explore the Home dashboard.
4. Open Myths or Creatures to browse stories.
5. Use the search bar or category filters to find specific content.
6. Select **Read Story** to view detailed information.
7. Open Regions to discover stories associated with Bhutanese places.
8. Take a quiz to check your understanding.
9. Save interesting stories to Favourites.
10. Use My Tasks to organise and track learning activities.

## 8. Technical Implementation

MythLab follows a modular structure in which different Python files handle different parts of the application.

The `main.py` file manages the main window and navigation between pages.

The `myths.py`, `creatures.py` and `myth_detail.py` files manage story collections, creature information and detailed story displays.

The `region.py` file handles regional exploration.

The `quiz.py` file provides the quiz interface and related interactions.

The `task.py` file manages learning tasks, while `favorites.py` handles saved stories.

SQLite is used for local data storage, including user-related information and personalised features.

The `assets` folder stores images used throughout the application.

## 9. Current Limitations

- MythLab is a desktop application and is not currently deployed as a public website.
- Some features depend on local image files and database availability.
- The collection of myths and regional stories is limited to the content included in the current version.
- The application does not currently provide automatic online updates to its story collection.
- It is primarily designed for computers with a supported Python environment.

## 10. Future Improvements

Possible future improvements include:

- Adding more Bhutanese myths and legends.
- Expanding the regional story collection.
- Introducing more quiz questions and difficulty levels.
- Improving accessibility and support for different screen sizes.
- Adding audio narration for stories.
- Providing multilingual content, including Dzongkha.
- Developing a web-based or mobile version.

## 11. Learning Outcomes

Developing MythLab provided practical experience in:

- Python GUI programming.
- Designing interactive interfaces.
- Organising code into modules.
- Handling images and other application resources.
- Using SQLite for local data management.
- Implementing search, filtering and navigation.
- Testing and debugging application features.
- Preparing software documentation.

## 12. References and Useful Resources

The following resources provide technical guidance and background information relevant to the project.

- Python Documentation: https://docs.python.org/3/
- Tkinter Documentation: https://docs.python.org/3/library/tkinter.html
- SQLite Documentation: https://www.sqlite.org/docs.html
- Pillow Documentation: https://pillow.readthedocs.io/
- CustomTkinter Documentation: https://customtkinter.tomschimansky.com/documentation/
- GitHub Documentation: https://docs.github.com/

The cultural stories and images used in MythLab should be credited to their original sources where applicable.

## 13. Conclusion

MythLab is an educational desktop application that combines cultural storytelling with interactive learning features. Through its myths, creatures, regional legends, quizzes, favourites and task management sections, the application provides users with an organised way to explore traditional stories.

The project demonstrates how Python GUI programming can be used to develop a culturally relevant learning application while applying important concepts such as interface design, modular programming, data storage and user interaction.