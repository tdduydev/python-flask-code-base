from myapi.extensions import db



class Categorynews(db.Model):

    __tablename__="Category_News"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("Categories.id"), nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey("News.id") , nullable=False)

    def __init__(self,  category_id: int = None,
                 news_id: int = None):
        self.category_id = category_id
        self.news_id = news_id

    def __str__(self) -> str:
        return 

    def __repr__(self) -> str:
        return "<Tag %s of News %s>" % self.category_id, self.news_id