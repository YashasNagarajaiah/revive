import streamlit as st
import cv2

def display_live_stream():

    st.title("Process Live Visual")

    # Dictionary of camera RTSP URLs
    camera_urls = {
        "Camera 1": "rtsp://admin:ict@2k19@192.168.70.5:554/Streaming/Channels/101",
        "Camera 2": "rtsp://admin:ict@2k19@192.168.70.5:554/Streaming/Channels/201",
        "Camera 3": "rtsp://admin:ict@2k19@192.168.70.5:554/Streaming/Channels/301",
        "Camera 4": "rtsp://admin:ict@2k19@192.168.70.5:554/Streaming/Channels/401",
    }

    # Dropdown to select a camera
    selected_camera = st.selectbox("Select Camera", list(camera_urls.keys()))

    # Get the RTSP URL for the selected camera (hidden from user)
    rtsp_url = camera_urls[selected_camera]

    # Button to start the stream
    if st.button("Start Stream"):
        # Open the RTSP stream
        video = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

        if not video.isOpened():
            st.error(f"Error: Unable to open video stream for {selected_camera}. Please check the camera settings.")
        else:
            st.success(f"Streaming {selected_camera}... Press 'Stop Stream' to exit.")
            stframe = st.empty()  # Placeholder for displaying frames
            stop_stream = st.button("Stop Stream")  # Button to stop the stream

            while True:
                ret, frame = video.read()
                if not ret:
                    st.error(f"Error: Unable to fetch frame from {selected_camera}. Exiting...")
                    break

                # Convert frame to RGB for Streamlit display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                stframe.image(frame_rgb, channels="RGB")

                # Stop streaming if the user clicks the stop button
                if stop_stream:
                    st.info(f"Stream for {selected_camera} stopped.")
                    break

            # Release the video capture resource
            video.release()


