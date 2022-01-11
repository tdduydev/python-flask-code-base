from myapi.extensions import db



class Tagnews(db.Model):

    __tablename__="Tag_News"
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("Tags.id"), nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey("News.id") , nullable=False)

    def __init__(self,  tag_id: int = None,
                 news_id: int = None):
        self.tag_id = tag_id
        self.news_id = news_id

    def __str__(self) -> str:
        return 

    def __repr__(self) -> str:
        return "<Tag %s of News %s>" % self.tag_id, self.news_id