from database import add_contact, get_contacts, update_chat_history
import sqlite3
from imports import *

class ContactFunctions:
    def add_contact(self):
        # Show a dialog box to enter the name of the new contact
        new_contact_name, ok = QInputDialog.getText(self, "Add Contact", "Enter the name of the new contact:")

        if ok and new_contact_name != "":
            # Check if the user exists in the database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (new_contact_name,))
            user = cursor.fetchone()
            conn.close()

        if user is None:
            # The user does not exist in the database
            QMessageBox.warning(self, "Error", "User does not exist.")
        elif new_contact_name in self.chat_history:
            # The user already exists in the conversation
            QMessageBox.warning(self, "Error", "User already exists in your conversation.")
        else:
            # Add the new contact to the contact list widget
            item = QListWidgetItem(new_contact_name)
            item.setSizeHint(item.sizeHint())
            self.contact_list_widget.addItem(item)

            # Create chat history for the new contact
            self.chat_history[new_contact_name] = []

            # Add the new contact to the database
            add_contact(self.username, new_contact_name)


    def delete_contact(self):
        # Get the selected contact's name
        selected_contact_name = self.contact_list_widget.currentItem().text()

        # Show a confirmation dialog box before deleting the contact
        reply = QMessageBox.question(
            self, "Delete Contact", f"Are you sure you want to delete {selected_contact_name}?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Remove the contact from the contact list widget
            selected_item = self.contact_list_widget.currentItem()
            self.contact_list_widget.takeItem(self.contact_list_widget.row(selected_item))

            # Remove the chat history of the selected contact
            del self.chat_history[selected_contact_name]

            # Clear the chat history widget
            self.chat_history_widget.clear()

            # Update the chat header with empty values
            chat_contact_name_label = self.chat_header_widget.findChild(QLabel)
            chat_contact_name_label.setText("")

            # Switch to the conversation list if there are no contacts left
            if self.contact_list_widget.count() == 0:
                self.stacked_widget.setCurrentWidget(self.conversation_list_widget)
            else:
                # Select the first contact in the list
                self.contact_list_widget.setCurrentRow(0)
                self.show_conversation()

            # Delete the contact from the database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM dashboard WHERE username=? AND contact=?", (self.username, selected_contact_name))
            conn.commit()
            conn.close()
        else:
            return
