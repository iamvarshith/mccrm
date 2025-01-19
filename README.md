# Insurance CRM System

A Customer Relationship Management (CRM) system designed for insurance agents to manage their clients, policies, and documents.

## Features

- User Authentication (Agents & Admins)
- Client Management
- Policy Management
  - Global Policies
  - Custom Client Policies
  - Policy Document Upload
- Dashboard Analytics
- Document Management
- Client Policy Assignment

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- SQLite3

## Installation

1. Clone the repository
`git clone https://github.com/yourusername/insurance-crm.git`
`cd insurance-crm`

2. Create a virtual environment
`python -m venv venv`

3. Activate the virtual environment

On Windows:
`venv\Scripts\activate`

On macOS/Linux:
`source venv/bin/activate`

4. Install required packages
`pip install -r requirements.txt`

5. Set up environment variables 


Create a .env file in the root directory
touch .env
Add the following variables to .env
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///instance/mccrm.db
6. Initialize the database
`flask db init`
`flask db migrate`
`flask db upgrade`


7. Create initial admin user
`flask create-admin`

## Running the Application

1. Start the development server
`flask run`

2. Access the application at `http://localhost:5000`

## Project Structure


insurance-crm/
├── app/
│ ├── init.py
│ ├── models/
│ │ └── models.py
│ ├── routes/
│ │ ├── auth.py
│ │ ├── clients.py
│ │ ├── dashboard.py
│ │ └── policies.py
│ ├── static/
│ ├── templates/
│ └── uploads/
├── instance/
├── migrations/
├── tests/
├── .env
├── .gitignore
├── config.py
├── requirements.txt
└── README.md



## Database Models

- Agent: Insurance agents and admin users
- Client: Insurance clients
- GlobalPolicy: System-wide policy templates
- UserPolicy: Client-specific policies
- AssignedPolicy: Policy assignments to clients

## API Routes

### Authentication
- `/auth/login` - Agent login
- `/auth/logout` - Agent logout

### Clients
- `/clients/` - List all clients
- `/clients/create` - Create new client
- `/clients/<id>` - View client details
- `/clients/<id>/edit` - Edit client details

### Policies
- `/policies/` - List all policies
- `/policies/create` - Create new policy
- `/policies/<id>` - View policy details
- `/policies/<id>/edit` - Edit policy details
- `/policies/download/<id>` - Download policy document

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make changes and commit (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please email support@example.com or create an issue in the GitHub repository.

## Authors

- Your Name - Initial work - [YourGitHub](https://github.com/yourusername)

## Acknowledgments

- Flask Documentation
- SQLAlchemy Documentation
- Bootstrap Documentation