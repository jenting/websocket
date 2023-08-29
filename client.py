import streamlit as st
import socketio

# Initialize a SocketIO client
sio = socketio.Client()

# Connect to the Flask-SocketIO server
sio.connect('http://localhost:8888')

# Streamlit UI
def main():
    st.set_page_config(page_title="WebSocket App")

    # st.title("WebSocket App Interacts With Flask-SocketIO")

    # Radio button to select an option
    selected_option = st.radio("Select an option:", ("One-Platform", "Platform"))

    # Button to trigger WebSocket event
    if st.button("Migrate"):
        send_websocket_event(selected_option)

# Function to send WebSocket event
def send_websocket_event(selected_option):
    if sio.connected:
        sio.emit('migrate_option', selected_option)
        st.success(f"Sent WebSocket message: {selected_option}")
    else:
        st.error("WebSocket is not connected")

if __name__ == '__main__':
    main()
