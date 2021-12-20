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
                "username": "admin",
                "email": "admin@gmail.com",
                "_password": pwd_context.hash("admin"),
                "lastname": "Extremely Best admin",
                "firstname": "Best admin",
                "address": generator.String("\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c"),
                "phonenumber": generator.String("123456")
            }
        )

        # Create 5 users
        for user in faker.create(1):
            # print("Adding user: %s" % user)
            self.db.session.add(user)
