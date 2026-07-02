import cv2
from cv2.typing import MatLike
from manga_ocr import MangaOcr
import PIL
from PIL import Image
from speech_bubble import find_bubbles, preprocess

#TODO: use multiprocessing?


def main():
    image1 = Image.open("sample/yfnu7-7(4).png")
    image2 = Image.open("sample/yfnu7-7(5).png")
    image3 = Image.open("sample/yfnu7-7(6).png")
    image4 = Image.open("sample/yfnu7-7(7).png")
    image5 = Image.open("sample/yfnu7-7(8).png")
    image6 = Image.open("sample/yfnu7-7(9).png")
    image7 = Image.open("sample/yfnu7-7(10).png")
    image8 = Image.open("sample/yfnu7-7(11).png")
    if image1 is not None:
        print(get_bubble_text([image1, image2, image3, image4, image5, image6, image7, image8]))
    

def resize_crops(cropped_images: list[MatLike], scale_factor: int = 2) -> list[MatLike]:
    resized_images: list[MatLike] = []
    for image in cropped_images:
        height, width = image.shape[:2]
        resized_image: MatLike = cv2.resize(
            image,
            (width * scale_factor, height * scale_factor),
            interpolation=cv2.INTER_LANCZOS4
        )
        resized_images.append(resized_image)
    return resized_images


def get_bubble_text(cropped_images) -> list[str]:
    mocr = MangaOcr()
    bubble_texts: list[str] = []
    for image in cropped_images:
        bubble_text = mocr(image)
        bubble_texts.append(bubble_text)
    return bubble_texts


if __name__ == "__main__":
    main()