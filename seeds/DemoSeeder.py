from flask_seeder import Seeder, Faker, generator

from myapi.models.user import User

from myapi.extensions import pwd_context


class DemoSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 10

    def run(self):
        # Create a new Faker and tell it how to create User objects
        faker = Faker(
            cls=User,
            init={
                "username": generator.Name(),
                "email": generator.String("\\c\\c\\c\\c\\c\\c\\c@gmail.com"),
                "_password": pwd_context.hash("123456789"),
                "last_name": generator.Name(),
                "first_name": generator.Name(),
                "address": generator.String("\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c"),
                "phone": generator.String("\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d")
            }
        )

        # Create 5 users
        for user in faker.create(50):
            # print("Adding user: %s" % user)
            self.db.session.add(user)
