from django.core.management.base import BaseCommand
from core.models import *

class Command(BaseCommand):
    help = 'Seeds the database with initial portfolio data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding portfolio data...')
        
        # Create Site Settings
        site_settings, created = SiteSettings.objects.get_or_create(
            id=1,
            defaults={
                'site_name': "Muwemi Ndovie - Mechanical Engineer",
                'hero_title': "Mechanical Engineering Innovator & Problem Solver",
                'hero_subtitle': "Specializing in hydraulic systems, automation, and sustainable energy solutions with a passion for innovation and efficiency",
                'about_title': "About Me",
                'about_subtitle': "Goal-oriented Mechanical Engineering student with distinction average and passion for sustainable innovation",
            }
        )
        
        # Create About Section
        about, created = About.objects.get_or_create(
            id=1,
            defaults={
                'content': "I am a goal-oriented, determined, and disciplined individual with a passion for problem-solving in the field of mechanical engineering. I possess strong ethical values and excel both in team settings and independently. I am committed to applying my skills and knowledge in engineering to deliver innovative and efficient solutions in design, development and maintenance of mechanical systems."
            }
        )
        
        # Create Skills
        skills_data = [
            # Engineering Skills
            {'name': 'Hydraulic System Design', 'category': 'ENG', 'level': 85},
            {'name': 'CAD (AutoCAD, Fusion360)', 'category': 'DESIGN', 'level': 80},
            {'name': 'MATLAB Simulation', 'category': 'ENG', 'level': 75},
            {'name': 'Fluid Mechanics', 'category': 'ENG', 'level': 80},
            {'name': 'Machine Element Design', 'category': 'ENG', 'level': 75},
            {'name': 'Strength of Materials', 'category': 'ENG', 'level': 80},
            
            # Programming Skills
            {'name': 'C++', 'category': 'PROG', 'level': 70},
            {'name': 'Arduino Programming', 'category': 'PROG', 'level': 75},
            {'name': 'HTML', 'category': 'PROG', 'level': 65},
            {'name': 'G-code', 'category': 'PROG', 'level': 70},
            
            # Manufacturing Skills
            {'name': 'Lathe Machine Operation', 'category': 'ENG', 'level': 70},
            {'name': 'Milling Machine Operation', 'category': 'ENG', 'level': 65},
            {'name': 'Shaper Machine Operation', 'category': 'ENG', 'level': 60},
            
            # Soft Skills
            {'name': 'Project Management', 'category': 'SOFT', 'level': 80},
            {'name': 'Team Leadership', 'category': 'SOFT', 'level': 85},
            {'name': 'Technical Communication', 'category': 'SOFT', 'level': 80},
            {'name': 'Problem Solving', 'category': 'SOFT', 'level': 90},
        ]
        
        for i, skill_data in enumerate(skills_data):
            Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults={**skill_data, 'order': i}
            )
        
        # Create Education
        education_data = [
            {
                'degree': 'Bachelor of Mechanical Engineering (Hons)',
                'institution': 'Malawi University of Business and Applied Sciences (MUBAS)',
                'period': 'January 2023 – October 2027',
                'description': 'Distinction average with distinctions in multiple core modules. Relevant modules: Computer Aided Drawing, Strength of Materials, Fluid Mechanics, Programming in C++, Machine Element Design, Engineering Materials.',
                'current': True,
                'order': 0
            }
        ]
        
        for edu in education_data:
            Education.objects.get_or_create(
                degree=edu['degree'],
                institution=edu['institution'],
                defaults=edu
            )
        
        # Create Certifications
        certifications_data = [
            {
                'title': 'Registered Student Engineer',
                'issuer': 'Malawi Engineering Institute',
                'issue_date': '2025-01-01',
                'in_progress': False
            },
            {
                'title': 'Artificial Intelligence',
                'issuer': 'Alison',
                'in_progress': True
            },
            {
                'title': 'Web Development',
                'issuer': 'W3 Schools',
                'in_progress': True
            },
        ]
        
        for cert in certifications_data:
            Certification.objects.get_or_create(
                title=cert['title'],
                issuer=cert['issuer'],
                defaults=cert
            )
        
        # Create Extracurricular Activities
        extracurriculars_data = [
            {
                'title': 'President, MUBAS Students Innovation Hub',
                'organization': 'Malawi University of Business and Applied Sciences',
                'role': 'President',
                'period': '2024 - Present',
                'description': 'Lead student innovation projects focused on engineering and technology. Coordinate workshops and mentorship programs that promote creativity, teamwork, and practical problem-solving.',
                'current': True,
                'order': 0
            },
            {
                'title': 'Founder and Coordinator, Peer Mentorship Program',
                'organization': 'MUBAS School of Engineering',
                'role': 'Founder & Coordinator',
                'period': '2024 - Present',
                'description': 'Established a mentorship program linking senior and junior engineering students for academic and career guidance. Oversee mentor-mentee pairings and facilitate sessions that build leadership and professional skills.',
                'current': True,
                'order': 1
            },
            {
                'title': 'Chess Team Captain',
                'organization': 'MUBAS',
                'role': 'Captain',
                'period': '2024 - Present',
                'description': 'Lead and manage the university\'s chess team, organizing practice sessions and competitive events. Foster teamwork, strategy development, and mentoring.',
                'current': True,
                'order': 2
            },
            {
                'title': 'Design Studio Participant',
                'organization': 'MUBAS Engineering Department',
                'role': 'Active Member',
                'period': '2023 - Present',
                'description': 'Actively engage in the design studio, working on projects involving designing and prototyping with Arduino technology. Collaborate with peers to develop innovative solutions.',
                'current': True,
                'order': 3
            },
        ]
        
        for activity in extracurriculars_data:
            Extracurricular.objects.get_or_create(
                title=activity['title'],
                organization=activity['organization'],
                defaults=activity
            )
        
        # Create Projects
        projects_data = [
            {
                'title': 'Hydropower Harnessing System from Domestic Water Flow',
                'short_description': 'Collaborated in a team to design a system capable of generating electrical power from household water flow.',
                'long_description': 'This group project involved designing a micro-hydropower system that can be integrated into domestic water supply systems. We conducted extensive calculations on flow rate, head pressure, and turbine efficiency to determine potential energy output. The project strengthened my teamwork, problem-solving, and technical report-writing skills in an engineering context.',
                'technologies': 'Turbine Design, Fluid Flow Analysis, Power Generation Concepts, CAD Modeling',
                'featured': True,
                'completion_date': '2024-06-01',
                'order': 0
            },
            {
                'title': 'Automated Locking System',
                'short_description': 'Designed and implemented an automated door locking system that enhances security through sensor-based access control.',
                'long_description': 'An individual project where I designed a complete automated locking system using Arduino microcontrollers. The system uses sensors to detect authorized access and controls a servo motor for locking mechanism. This project provided hands-on experience with microcontroller programming, sensor integration, and mechanical-electronic system design.',
                'technologies': 'Arduino, Sensors, Servo Motor, C++ Programming, Circuit Design',
                'featured': True,
                'github_url': '',
                'completion_date': '2024-03-01',
                'order': 1
            },
            {
                'title': 'Automated Retractable Washing Line',
                'short_description': 'Developed a functional prototype that automatically retracts the washing line under shelter during rainfall.',
                'long_description': 'This prototype project involved creating an intelligent washing line system that automatically retracts when rain is detected and extends when conditions are dry. I designed both the mechanical layout and electrical control system, integrating water sensors with servo motors. The project provided practical experience in automation, environmental sensing, and prototype development.',
                'technologies': 'Arduino Uno, Water Sensor, Servo Motor, Mechanical Design, Prototyping',
                'featured': True,
                'completion_date': '2024-01-01',
                'order': 2
            },
        ]
        
        for project_data in projects_data:
            project, created = Project.objects.get_or_create(
                title=project_data['title'],
                defaults=project_data
            )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully seeded portfolio data!')
        )