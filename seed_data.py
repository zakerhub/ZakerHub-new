import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from academics.models import Curriculum, Subject, Course, Level, CourseItem
from subscriptions.models import SubscriptionOption
from django.utils import timezone

User = get_user_model()

def seed():
    print("Starting data seeding...")

    # 1. Create Levels
    basic, _ = Level.objects.get_or_create(name='BASIC')
    advanced, _ = Level.objects.get_or_create(name='ADVANCED')
    print("Levels created.")

    # 2. Create Users
    admin, created = User.objects.get_or_create(
        email='admin@zakerhub.com',
        defaults={
            'username': 'admin@zakerhub.com',
            'name': 'System Admin',
            'role': 'ADMIN',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()

    teacher1, created = User.objects.get_or_create(
        email='teacher1@zakerhub.com',
        defaults={
            'username': 'teacher1@zakerhub.com',
            'name': 'Dr. Ahmed Math',
            'role': 'TEACHER'
        }
    )
    if created:
        teacher1.set_password('teacher123')
        teacher1.save()

    teacher2, created = User.objects.get_or_create(
        email='teacher2@zakerhub.com',
        defaults={
            'username': 'teacher2@zakerhub.com',
            'name': 'Prof. Sarah Physics',
            'role': 'TEACHER'
        }
    )
    if created:
        teacher2.set_password('teacher123')
        teacher2.save()
        
    student1, created = User.objects.get_or_create(
        email='student1@zakerhub.com',
        defaults={
            'username': 'student1@zakerhub.com',
            'name': 'John Student',
            'role': 'STUDENT'
        }
    )
    if created:
        student1.set_password('student123')
        student1.save()

    print("Users created.")

    # 3. Create Curriculums
    igcse, _ = Curriculum.objects.get_or_create(code='IGCSE', defaults={'name': 'IGCSE / IG'})
    american, _ = Curriculum.objects.get_or_create(code='AD', defaults={'name': 'American Diploma (AD)'})
    ib, _ = Curriculum.objects.get_or_create(code='DP', defaults={'name': 'IB Diploma Programme (DP)'})
    print("Curriculums created.")

    # 4. Create Subjects
    math_sub, _ = Subject.objects.get_or_create(name='Mathematics', curriculum=igcse)
    physics_sub, _ = Subject.objects.get_or_create(name='Physics', curriculum=igcse)
    history_sub, _ = Subject.objects.get_or_create(name='World History', curriculum=american)
    print("Subjects created.")

    # 5. Create Courses
    course1, _ = Course.objects.get_or_create(
        subject=math_sub,
        teacher=teacher1,
        defaults={'description': 'Advanced Mathematics for IGCSE Students.'}
    )
    
    course2, _ = Course.objects.get_or_create(
        subject=physics_sub,
        teacher=teacher2,
        defaults={'description': 'Comprehensive Physics course covering all IGCSE topics.'}
    )
    print("Courses created.")

    # 6. Create Subscription Options
    SubscriptionOption.objects.get_or_create(
        course=course1,
        level=advanced,
        defaults={
            'plan_type': 'MONTHLY',
            'price': 500.00,
            'duration_days': 30
        }
    )
    
    SubscriptionOption.objects.get_or_create(
        course=course2,
        level=basic,
        defaults={
            'plan_type': 'MONTHLY',
            'price': 450.00,
            'duration_days': 30
        }
    )
    print("Subscription Options created.")

    # 7. Create Course Items
    CourseItem.objects.get_or_create(
        course=course1,
        title='Welcome to Math IGCSE',
        defaults={
            'type': 'ANNOUNCEMENT',
            'level': None
        }
    )
    
    CourseItem.objects.get_or_create(
        course=course1,
        title='Algebra Basics - Week 1',
        defaults={
            'type': 'MATERIAL',
            'level': advanced
        }
    )
    
    CourseItem.objects.get_or_create(
        course=course2,
        title='Forces and Motion Notes',
        defaults={
            'type': 'MATERIAL',
            'level': basic
        }
    )
    print("Course Items created.")

    print("Seeding completed successfully!")

if __name__ == '__main__':
    seed()
