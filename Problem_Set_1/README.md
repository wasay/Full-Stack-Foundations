# Full-Stack-Foundations
Solution Code to Full Stack Foundations (ud088)

# Notes on how to run Problem Set 1

python main.py
python puppypopulator.py
python main.py

# test migrations
python migrations/manage.py test

# run migrations
python migrations/manage.py upgrade
python main.py

# populate additional data
python add_data.py
python main.py

# check-in puppy into a shelter
python checkin.py <puppy_name> <shelter_name>
python main.py

# transfer puppies evenly
python transfer_evenly.py
python main.py