# to run flask ui via VScode or other IDE
- First run app.py 
- Then use the following link for the app: http://127.0.0.1:5001/checkphishing

# Run via VM
- start the VM instance
- Use the SSH connect
- Run the following code:
  - git clone https://github.com/Sanderror/Data-engineering.git (Does not work need password or something)
  - cd Data-engineering/flask-ui-v1
  - sudo apt install python3.12-venv
  - python3 -m venv .venv
  - source .venv/bin/activate
  - pip install -r requirements.txt
  - python3 app.py
 - Go to the following link http://vm_external_ip:5001/checkphishing (use your own vm external IP address)
