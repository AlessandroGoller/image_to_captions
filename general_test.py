from app.crud.company import get_company_by_user_id
from app.crud.instagram import insert_data_to_db, get_instagram_by_id
from app.crud.user import get_user_by_email
from app.services.ig_scraping import GetInstagramProfile

username = "dulacetduparc"
client = GetInstagramProfile()

# instagram = get_instagram_by_id(id_instagram=1)
# print(instagram.post)

data = client.get_post_info_json(username,last_n_posts=100)
user_id = get_user_by_email(email="riccardoriccicalavino@gmail.com").user_id
company_id = get_company_by_user_id(user_id=user_id).id_company
if insert_data_to_db(data=data,user_id=user_id,company_id=company_id):
    print('Aggiunto correttamente nel db')
else:
    print('Errorr')

