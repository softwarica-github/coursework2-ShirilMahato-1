from imports import*
from unit_test import *
from int_test import*



if __name__ == '__main__':
    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Run the unittests
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestChatNamespace))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestContactFunctions))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestEncryptionManager))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestLoginWindow))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestSignupWindow))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestMainWindow))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestChatHeaderWidgetIntegration))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestEncryptionManagerIntegration))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestSignupWindowIntegration))

    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)

    if test_result.wasSuccessful():
        # app = QApplication(sys.argv)
        signup_window = SignupWindow(None)  # Temporarily pass None
        login_window = LoginWindow(signup_window)
        signup_window.login_window = login_window  # Now that login_window exists, assign it to signup_window
        login_window.show()
        sys.exit(app.exec_())