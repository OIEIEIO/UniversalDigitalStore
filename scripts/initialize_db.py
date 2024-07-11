from api.app import create_app, db
from data.models import Order

app = create_app()
app.app_context().push()
db.create_all()
