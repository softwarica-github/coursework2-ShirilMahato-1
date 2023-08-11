from database import update_chat_history
from imports import *
class ChatFunctions:
    def send_message(self):
        # Get the selected contact's name
        selected_contact_name = self.contact_list_widget.currentItem().text()

        # Get the text from the chat input widget
        message_text = self.chat_input_widget.text().strip()

        if message_text != "":
            # Encrypt the message before storing it
            encrypted_message = self.encrypt_message(message_text)

            # Add the message to the chat history of the selected contact
            self.chat_history[selected_contact_name].append(f"{self.username}: {encrypted_message}")

            # Display the chat history of the selected contact
            self.display_chat_history(selected_contact_name)

            # Clear the chat input widget
            self.chat_input_widget.clear()

            # Send the message to the server
            self.socketio.emit(
                'register',
                {'username': self.username},
                namespace='/chat'
            )

            # Update the chat history in the database
            update_chat_history(
                self.username,
                selected_contact_name,
                "\n".join(self.chat_history[selected_contact_name])
            )

            self.socketio.emit(
                'message',
                {
                    'text': f"{self.username}: {encrypted_message}",
                    'recipient': selected_contact_name
                },
                namespace='/chat'
            )

    def receive_message(self, data):
        # Get the sender's username and the message text
        sender, message_text = data.split(": ", 1)

        # Encrypt the received message before storing it
        encrypted_message = self.encrypt_message(message_text)

        # Update the chat history in the database
        update_chat_history(
            self.username,
            sender,
            "\n".join(self.chat_history[sender])
        )

        # Decrypt the message for displaying in the GUI
        decrypted_message = self.decrypt_message(encrypted_message)

        # Add the message to the chat history of the sender
        if sender not in self.chat_history:
            self.chat_history[sender] = []
        self.chat_history[sender].append(f"{sender}: {decrypted_message}")

        self.update_gui_signal.emit(sender)

    def show_conversation(self):
        # Get the selected contact's name
        selected_item = self.contact_list_widget.currentItem()
        if selected_item is None:
            return

        selected_contact_name = selected_item.text()

        # Check if the contact still exists in chat_history
        if selected_contact_name in self.chat_history:
            # Update the chat header with the selected contact's name
            chat_contact_name_label = self.chat_header_widget.findChild(QLabel)
            chat_contact_name_label.setText(selected_contact_name)

            # Display the chat history of the selected contact
            self.display_chat_history(selected_contact_name)

            # Switch to the chat display
            self.stacked_widget.setCurrentWidget(self.chat_widget)

    def display_chat_history(self, contact_name):
        # Clear the chat history widget
        self.chat_history_widget.clear()

        # Retrieve the chat history for the selected contact
        chat_history = self.chat_history[contact_name]

        # Display each message in the chat history
        for message in chat_history:
            if message.startswith("File Sent: "):
                # If it's a file, show the file path as a clickable link
                file_path = message.replace("File Sent: ", "")
                self.chat_history_widget.append(f'<a href="file:{file_path}">{file_path}</a>')
            else:
                # Split the message into sender and text if possible
                parts = message.split(": ", 1)
                if len(parts) == 2:
                    sender, text = parts
                    # Decrypt the message before displaying it
                    decrypted_message = self.decrypt_message(text)
                    # Create a formatted message with sender name and decrypted text
                    formatted_message = f"<b>{sender}</b>: {decrypted_message}"
                else:
                    # The message does not follow the expected format, append as is
                    formatted_message = message

                # Append the formatted message to the chat history widget
                self.chat_history_widget.append(formatted_message)

            self.chat_history_widget.append("")
