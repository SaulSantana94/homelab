Ansible Playbook Setup Readme
This README provides instructions for deploying using Ansible playbooks. Please follow the steps below for a successful deployment.

Prerequisites
Ansible installed on your local machine.
Access to the required secrets stored in pass for deployment.
Knowledge of how to obtain Telegram chat_id and token.
Steps to Deploy
Access the Metal Folder

Navigate to the metal folder in your terminal.
Install pass

If pass is not already installed on your system, follow the installation instructions for your operating system:
For Debian/Ubuntu:
shell
Copy code
sudo apt-get install pass
For Fedora/RHEL:
shell
Copy code
sudo dnf install pass
For macOS (via Homebrew):
shell
Copy code
brew install pass
For other systems, refer to the pass GitHub page for installation instructions.
Set Secrets in pass

Use the pass command-line tool to set the following secrets:
k8s.dabol/telegram/chat_id
k8s.dabol/telegram/token
k8s.dabol/prepare_password
k8s.dabol/smtp
For example:
shell
Copy code
pass insert k8s.dabol/telegram/chat_id
Run Prepare Playbook

Execute the following command to prepare the deployment:
shell
Copy code
make prepare
Run Cluster Playbook

Once the preparation is complete, run the following command to deploy the cluster:
shell
Copy code
make cluster
About Ansible
Ansible is an open-source automation tool used for configuration management, application deployment, and task automation. It allows you to automate repetitive tasks, making it easier to manage and deploy infrastructure.

About pass
pass is a simple command-line password manager for Unix systems. It stores each password in a GPG-encrypted file and allows you to organize them into folders. In this setup, pass is used to securely store sensitive information such as API tokens and passwords required for deployment.

Obtaining Telegram chat_id and token
To obtain the Telegram chat_id and token, follow these steps:

Create a Telegram Bot:
Start a conversation with the BotFather on Telegram.
Use the /newbot command to create a new bot and follow the instructions.
Once the bot is created, BotFather will provide you with a token.
Get Chat ID:
Add your bot to the desired Telegram group or channel.
Send a message to the group/channel.
Use the following API call to get the chat_id:
shell
Copy code
curl https://api.telegram.org/bot<YOUR_TOKEN_HERE>/getUpdates
Look for the chat object within the response JSON. The id field within the chat object represents the chat_id of the group/channel.
Make sure to keep the token and chat_id secure and not expose them publicly. These credentials are required for integrating Telegram notifications with your deployment setup.