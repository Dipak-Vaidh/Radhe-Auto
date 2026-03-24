"""
Load demo data for local/testing. Safe: skips if cars already exist unless --force.

Usage:
  python manage.py seed_demo_data
  python manage.py seed_demo_data --force   # clears cars-related data first
"""
from decimal import Decimal
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from PIL import Image

from cars.models import Brand, CarModel, Car, CarImage, Inquiry, Testimonial


def _placeholder_file(name='demo.png'):
    buf = BytesIO()
    Image.new('RGB', (200, 200), color=(220, 220, 230)).save(buf, format='PNG')
    buf.seek(0)
    return ContentFile(buf.read(), name=name)


class Command(BaseCommand):
    help = 'Insert bulk demo data (brands, models, cars, images, inquiries, testimonials)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Delete existing demo-related rows then re-seed',
        )

    def handle(self, *args, **options):
        if options['force']:
            self._clear()
        elif Car.objects.exists():
            self.stdout.write(self.style.WARNING('Data already exists. Use --force to replace.'))
            return

        user, _ = User.objects.get_or_create(
            username='demo_seller',
            defaults={'email': 'demo@radheauto.com', 'is_staff': False},
        )
        if not user.has_usable_password():
            user.set_password('unused-demo')
            user.save()

        brands_data = [
            ('Maruti Suzuki', ['Swift', 'Baleno', 'Dzire']),
            ('Hyundai', ['i20', 'Creta', 'Venue']),
            ('Tata', ['Nexon', 'Punch']),
            ('Honda', ['City', 'Amaze']),
        ]

        brands = {}
        for bname, models_list in brands_data:
            b, _ = Brand.objects.get_or_create(name=bname)
            brands[bname] = b
            for mname in models_list:
                CarModel.objects.get_or_create(brand=b, name=mname)

        # External image URLs (no upload needed for CarImage)
        img_urls = [
            'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800',
            'https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800',
            'https://images.unsplash.com/photo-1583121274602-3e2820c69888?w=800',
        ]

        cars_spec = [
            ('Maruti Suzuki', 'Swift', '2022 Maruti Swift VXI – Single owner', 2022, 'VXI', Decimal('625000'), Decimal('695000'), 18500, 'Petrol', 'MT', 'Hatchback', '1st Owner', True),
            ('Hyundai', 'Creta', '2021 Hyundai Creta SX – Well maintained', 2021, 'SX', Decimal('1320000'), Decimal('1450000'), 32000, 'Diesel', 'AT', 'SUV', '1st Owner', True),
            ('Tata', 'Nexon', '2023 Tata Nexon XZ+ Dark Edition', 2023, 'XZ+', Decimal('985000'), None, 12000, 'Petrol', 'AT', 'SUV', '1st Owner', False),
            ('Honda', 'City', '2020 Honda City ZX CVT', 2020, 'ZX CVT', Decimal('1120000'), Decimal('1250000'), 45000, 'Petrol', 'AT', 'Sedan', '2nd Owner', True),
            ('Maruti Suzuki', 'Baleno', '2019 Baleno Alpha – Low KM', 2019, 'Alpha', Decimal('545000'), Decimal('595000'), 42000, 'Petrol', 'MT', 'Hatchback', '2nd Owner', False),
            ('Hyundai', 'i20', '2023 i20 Sportz IVT', 2023, 'Sportz IVT', Decimal('875000'), None, 8000, 'Petrol', 'AT', 'Hatchback', '1st Owner', False),
        ]

        for i, spec in enumerate(cars_spec):
            bname, mname, title, year, variant, price, orig, km, fuel, trans, body, owner, featured = spec
            brand = brands[bname]
            model = CarModel.objects.get(brand=brand, name=mname)
            car = Car.objects.create(
                seller=user,
                title=title,
                brand=brand,
                model=model,
                year=year,
                variant=variant,
                price=price,
                original_price=orig,
                mileage=km,
                fuel_type=fuel,
                transmission=trans,
                body_type=body,
                ownership=owner,
                color='White',
                city='Ahmedabad',
                registration_state='GJ',
                contact_name='Demo Seller',
                contact_number='9876543210',
                description='Demo listing for testing. Vehicle in good condition.',
                is_featured=featured,
                status='APPROVED',
            )
            for j, url in enumerate(img_urls):
                CarImage.objects.create(
                    car=car,
                    image_url=url,
                    is_primary=(j == 0),
                )

        Inquiry.objects.create(
            first_name='Rahul',
            last_name='Shah',
            email='rahul@example.com',
            phone='9123456789',
            subject='buy',
            message='Interested in Swift. Please call.',
        )
        Inquiry.objects.create(
            first_name='Priya',
            last_name='Mehta',
            email='priya@example.com',
            phone='9988776655',
            subject='sell',
            message='Want to sell my car.',
        )

        for order, (name, desig) in enumerate([
            ('Amit Patel', 'Business owner'),
            ('Sneha Desai', 'IT professional'),
            ('Vikram Singh', 'Doctor'),
            ('Kavya Nair', 'Teacher'),
        ]):
            Testimonial.objects.create(
                name=name,
                designation=desig,
                is_active=True,
                order=order,
                image=_placeholder_file(f'testimonial_{order}.png'),
            )

        self.stdout.write(self.style.SUCCESS('Demo data loaded: brands, cars, inquiries, testimonials.'))

    def _clear(self):
        CarImage.objects.all().delete()
        Car.objects.all().delete()
        CarModel.objects.all().delete()
        Brand.objects.all().delete()
        Inquiry.objects.all().delete()
        Testimonial.objects.all().delete()
        self.stdout.write('Cleared cars, brands, inquiries, testimonials.')
