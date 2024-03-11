from database import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    company_email = db.Column(db.String(200), nullable=False)
    product_title = db.Column(db.String(500), nullable=False)
    product_logo = db.Column(db.Text, nullable=True)
    product_url = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    twitter_username = db.Column(db.Text, nullable=True)
    unique_tag = db.Column(db.Text, nullable=True)
    common_tags = db.Column(db.Text, nullable=True)
    platform = db.Column(db.Text, nullable=True)
    post_id = db.Column(db.Text, nullable=True)
    gen_description = db.Column(db.Text, nullable=True)
    tel_group = db.Column(db.String(200), nullable=True)
    def __repr__(self):
        return f'<Product {self.id}>'
    
    def serialize(self):
        """Serialize the Product object to a JSON format."""
        return {
            'id': self.id,
            'company_name': self.company_name,
            'company_email': self.company_email,
            'product_title': self.product_title,
            'product_logo': self.product_logo,
            'product_url': self.product_url,
            'description': self.description,
            'twitter_username': self.twitter_username,
        }
    
class Fan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    interests = db.Column(db.String(255))
    engagement_level = db.Column(db.Integer)

    def __init__(self, email, interests, engagement_level):
        self.email = email
        self.interests = interests
        self.engagement_level = engagement_level


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    product_images = db.Column(db.Text, nullable=False)
    videos = db.Column(db.Text, nullable=False)
    product_landing_page = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)


    def __repr__(self):
        return f'<Campaign {self.id}>'
    
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer)
    username = db.Column(db.String(255))
    comment_id = db.Column(db.Integer)
    content = db.Column(db.Text)
    full_content = db.Column(db.Text)
    parent_id = db.Column(db.Integer)
    sentiment = db.Column(db.Text, nullable=True)
    reply_message_id = db.Column(db.Integer)
    reply_message = db.Column(db.Text, nullable=True)
    
    def __init__(self, account_id, username, comment_id, content, full_content, parent_id):
        self.account_id = account_id
        self.username = username
        self.comment_id = comment_id
        self.content = content
        self.full_content = full_content
        self.parent_id = parent_id
        
    def serialize(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'username': self.username,
            'comment_id': self.comment_id,
            'content': self.content,
            'full_content': self.full_content,
            'parent_id': self.parent_id,
            'sentiment': self.sentiment,
            'reply_message_id': self.reply_message_id,
            'reply_message': self.reply_message
        }