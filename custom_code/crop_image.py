def crop_and_save_image_pil(image_path, num_crops_width, num_crops_height, save_dir='D:/cropped_images'):
    full_name = os.path.basename(image_path)
    file_name, _ = os.path.splitext(full_name)

    # 이미지 불러오기
    with Image.open(image_path) as img:
        img_width, img_height = img.size

        # 자르기 위한 단일 조각의 크기 계산
        crop_width = img_width // num_crops_width
        crop_height = img_height // num_crops_height

        # 저장 디렉터리 생성
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # 이미지 자르기 및 저장
        crop_num = 0
        for i in tqdm(range(num_crops_height)):
            for j in range(num_crops_width):
                left = j * crop_width
                upper = i * crop_height
                right = (j + 1) * crop_width
                lower = (i + 1) * crop_height

                # 자르기
                crop_img = img.crop((left, upper, right, lower))

                # 자른 이미지 파일명 생성 및 저장
                crop_img_filename = f"{save_dir}/{file_name}_crop_{crop_num}.bmp"
                crop_img.save(crop_img_filename)
                crop_num += 1
