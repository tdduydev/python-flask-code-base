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
                "username": generator.String("\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c"),
                "email": generator.String("\\c\\c\\c\\c\\c\\c\\c@gmail.com"),
                "_password": pwd_context.hash("admin"),
                "lastname": generator.Name(),
                "firstname": generator.Name(),
                "address": generator.String("\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c"),
                "phonenumber": generator.String("\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d")
            }
        )
        # Create 1000 users
        # for user in faker.create(1000):
        #     # print("Adding user: %s" % user)
        #     self.db.session.add(user)

        adminfaker = Faker(
            cls=User,
            init={
                "username": "normal",
                "email": generator.String("normal@gmail.com"),
                "_password": pwd_context.hash("normal"),
                "lastname": "normal",
                "firstname": "normal",
                "address": generator.String("\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c"),
                "phonenumber": generator.String("\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d")
            }
        )

        for user in adminfaker.create(1):
            self.db.session.add(user)
