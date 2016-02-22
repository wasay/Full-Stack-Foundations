# Full-Stack-Foundations
Solution Code to Full Stack Foundations (ud088)

# Notes on how to run Problem Set 2
# This paws application is the folder "Problem_Set_2" renamed to paws

python main.py
python puppypopulator.py
python main.py

# test migrations
python migrations/manage.py test

# run migrations
python migrations/manage.py upgrade
python main.py

# populate adoptors
python data_add_adoptors.py
python main.py

# populate puppy adoptors
python data_add_puppy_adoptors.py
python main.py

# update shelter capacity numbers
python data_reset_shelter_capacity.py
python main.py

# check-in a puppy into a shelter
# python checkin.py <puppy_name> <shelter_name>
python checkin.py Zoey "Oakland Animal Services"
 
python main.py

# transfer puppies evenly
python transfer_evenly.py
python main.py