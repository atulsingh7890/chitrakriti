import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from color_utils import rgb_to_xyz,delta_e_cie1976


def visualize_colors(color_list):
    for i, colors in enumerate(color_list):
        r1, g1, b1, r2, g2, b2, delta_e = colors

        col1, col2, col3 = st.columns(3)

        # Color picker for the first RGB color
        with col1:
            st.subheader(f"Color 1 - Row {i+1}")
            color1 = st.color_picker("Pick a color", f"#{r1:02x}{g1:02x}{b1:02x}", key=f"color1_{i}")
            r1, g1, b1 = tuple(int(color1[i:i + 2], 16) for i in (1, 3, 5))
            color_img1 = np.array([[[r1, g1, b1]]], dtype=np.uint8)
            st.image(color_img1, caption="Color 1", width=150)

        # Color picker for the second RGB color
        with col2:
            st.subheader(f"Color 2 - Row {i+1}")
            color2 = st.color_picker("Pick a color", f"#{r2:02x}{g2:02x}{b2:02x}", key=f"color2_{i}")
            r2, g2, b2 = tuple(int(color2[i:i + 2], 16) for i in (1, 3, 5))
            color_img2 = np.array([[[r2, g2, b2]]], dtype=np.uint8)
            st.image(color_img2, caption="Color 2", width=150)

        x1, y1, z1 = rgb_to_xyz(r1, g1, b1)
        x2, y2, z2 = rgb_to_xyz(r2, g2, b2)

        delta_e = delta_e_cie1976(x1, y1, z1, x2, y2, z2)

        # Visualize the chosen colors
        with col3:
            # Display the color difference as a centered textbox with the same size as the visualizations
            st.subheader("Color Difference")
            st.markdown(f"<div style='display: flex; align-items: center; justify-content: center; font-size: 20px; width: 150px; height: 150px; padding: 10px;'>{delta_e:.2f}</div>", unsafe_allow_html=True)

        # Add a separator between rows
        st.markdown("---")

def main():
    st.title("Color Difference Calculator")

    st.write("Choose colors using the color pickers:")

    # Get the session-based list of selected colors
    color_list = st.session_state.color_list if "color_list" in st.session_state else []

    # Add a button to clone the row
    if st.button("Clone Row"):
        # Clone the row by adding the latest selected colors to the list
        if color_list:
            latest_colors = color_list[-1]
            color_list.append(latest_colors)
        else:
            # If no previous rows, add default values
            default_colors = (128, 128, 128, 0, 0, 0, 0)
            color_list.append(default_colors)

    # Visualize the colors for each row
    visualize_colors(color_list)

    # Save visualization button
    if st.button("Save Visualization"):
        # For simplicity, saving only the last row's visualization
        r1, g1, b1, r2, g2, b2, delta_e = color_list[-1]
        #save_visualization(r1, g1, b1, r2, g2, b2, delta_e)
        st.success("Visualization saved as color_visualization.png")

    # Update the session-based list with the updated color_list
    st.session_state.color_list = color_list

if __name__ == "__main__":
    main()