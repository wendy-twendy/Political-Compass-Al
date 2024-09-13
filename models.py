from app import db
from datetime import datetime

class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    education = db.Column(db.String(50))
    city = db.Column(db.String(50))
    answers = db.Column(db.JSON)
    economic_score = db.Column(db.Float)
    libertarian_authoritarian_score = db.Column(db.Float)
    completion_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserData {self.id}>'

# Add questions and municipalities lists here
questions = [
    "The free market is the most effective way to distribute resources.",
    "Government intervention in the economy is necessary to protect citizens.",
    "Private property rights should be protected at all costs.",
    "A strong welfare system is essential for a just society.",
    "Corporations should be subject to strict regulations.",
    "Labor unions are essential for protecting workers' rights.",
    "Taxation is a form of theft.",
    "Universal healthcare should be provided by the government.",
    "Education should be privatized.",
    "Environmental regulations are necessary to combat climate change.",
    "The government should have a strong military presence.",
    "Police powers should be limited to protect civil liberties.",
    "Freedom of speech should be absolute, with no restrictions.",
    "The death penalty is a just form of punishment for severe crimes.",
    "Gun ownership is a fundamental right that should not be infringed upon.",
    "Same-sex marriage should be legally recognized.",
    "Abortion should be legal and accessible.",
    "Immigration policies should be more restrictive.",
    "Racial and ethnic minorities should receive special protections.",
    "Religion should play a role in government policy-making."
]

municipalities = [
    "Belsh", "Berat", "Bulqizë", "Cërrik", "Delvinë", "Devoll", "Dibër",
    "Dimal", "Divjakë", "Dropull", "Durrës", "Elbasan", "Fier", "Finiq",
    "Fushë-Arrëz", "Gjirokastër", "Gramsh", "Has", "Himarë", "Kamëz", "Kavajë",
    "Këlcyrë", "Klos", "Kolonjë", "Konispol", "Korçë", "Krujë", "Kuçovë",
    "Kukës", "Kurbin", "Lezhë", "Libohovë", "Librazhd", "Lushnjë",
    "Malësi e Madhe", "Maliq", "Mallakastër", "Mat", "Memaliaj", "Mirditë",
    "Patos", "Peqin", "Përmet", "Pogradec", "Poliçan", "Prrenjas", "Pukë",
    "Pustec", "Roskovec", "Rrogozhinë", "Sarandë", "Selenicë", "Shijak",
    "Shkodër", "Skrapar", "Tepelenë", "Tiranë", "Tropojë", "Vau i Dejës",
    "Vlorë", "Vorë"
]
