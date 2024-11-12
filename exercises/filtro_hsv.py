"""

Pequeño script para filtros HSV

"""

import cv2
import numpy as np
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Pequeño script para filtros HSV")
    parser.add_argument(
        "--image", help="Path a la imagen a utilizar", default="screen.png"
    )
    args = parser.parse_args()

    # Create image
    img = cv2.imread(args.image)

    # Create a window
    cv2.namedWindow("image")

    # create trackbars for color change
    cv2.createTrackbar(
        "HMin", "image", 0, 179, lambda x: x
    )  # Hue is from 0-179 for Opencv
    cv2.createTrackbar("HMax", "image", 0, 179, lambda x: x)

    cv2.createTrackbar("SMin", "image", 0, 255, lambda x: x)
    cv2.createTrackbar("SMax", "image", 0, 255, lambda x: x)

    cv2.createTrackbar("VMin", "image", 0, 255, lambda x: x)
    cv2.createTrackbar("VMax", "image", 0, 255, lambda x: x)

    # Set default value for MAX HSV trackbars.
    cv2.setTrackbarPos("HMax", "image", 179)
    cv2.setTrackbarPos("SMax", "image", 255)
    cv2.setTrackbarPos("VMax", "image", 255)

    # Initialize to check if HSV min/max value changes
    hMin = sMin = vMin = hMax = sMax = vMax = 0
    phMin = psMin = pvMin = phMax = psMax = pvMax = 0

    output = img
    waitTime = 33

    while True:
        # get current positions of all trackbars
        hMin = cv2.getTrackbarPos("HMin", "image")
        sMin = cv2.getTrackbarPos("SMin", "image")
        vMin = cv2.getTrackbarPos("VMin", "image")

        hMax = cv2.getTrackbarPos("HMax", "image")
        sMax = cv2.getTrackbarPos("SMax", "image")
        vMax = cv2.getTrackbarPos("VMax", "image")

        # Set minimum and max HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        # Create HSV Image and threshold into a range.
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(img, img, mask=mask)

        # Print if there is a change in HSV value
        if (
            phMin != hMin
            or psMin != sMin
            or pvMin != vMin
            or phMax != hMax
            or psMax != sMax
            or pvMax != vMax
        ):
            print(
                f"(hMin = {hMin} , sMin = {sMin}, vMin = {vMin}), "
                f"(hMax = {hMax} , sMax = {sMax}, vMax = {vMax})"
            )
            phMin, psMin, pvMin = hMin, sMin, vMin
            phMax, psMax, pvMax = hMax, sMax, vMax
        # Display output image
        cv2.imshow("image", output)

        # Wait longer to prevent freeze for videos.
        if cv2.waitKey(waitTime) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
