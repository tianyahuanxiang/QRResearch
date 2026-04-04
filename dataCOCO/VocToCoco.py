import os
import json
import xml.etree.ElementTree as ET
from tqdm import tqdm

def xml_to_coco(xml_dir, output_json):
    """ 将 XML 文件转换为 COCO 格式 JSON """
    # 初始化 COCO 结构
    coco = {
        "images": [],
        "annotations": [],
        "categories": []
    }

    # 类别映射（根据你的数据集类别调整）
    categories = {
        "QR": 1,
        # ... 其他类别
    }
    for name, cid in categories.items():
        coco["categories"].append({"id": cid, "name": name})

    # 图像和标注 ID 计数器
    image_id = 1
    annotation_id = 1

    # 遍历 XML 文件
    for xml_file in tqdm(os.listdir(xml_dir)):
        if not xml_file.endswith(".xml"):
            continue
        xml_path = os.path.join(xml_dir, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 提取图像信息
        filename = root.find("filename").text
        size = root.find("size")
        width = int(size.find("width").text)
        height = int(size.find("height").text)

        # 添加图像信息
        coco["images"].append({
            "id": image_id,
            "file_name": filename,
            "width": width,
            "height": height
        })

        # 提取目标标注
        for obj in root.findall("object"):
            name = obj.find("name").text
            bbox = obj.find("bndbox")
            xmin = int(bbox.find("xmin").text)
            ymin = int(bbox.find("ymin").text)
            xmax = int(bbox.find("xmax").text)
            ymax = int(bbox.find("ymax").text)
            width = xmax - xmin
            height = ymax - ymin

            # 添加标注信息
            coco["annotations"].append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": categories[name],
                "bbox": [xmin, ymin, width, height],
                "area": width * height,
                "iscrowd": 0
            })
            annotation_id += 1

        image_id += 1

    # 保存 JSON
    with open(output_json, "w") as f:
        json.dump(coco, f, indent=4)

def main():
    base_dir = r"E:\University\QR\RT-DETRs\dataCOCO"
    label_dir = os.path.join(base_dir, "label")
    annotations_dir = os.path.join(base_dir, "annotations")

    # 创建 annotations 目录（如果不存在）
    os.makedirs(annotations_dir, exist_ok=True)

    # 转换训练集
    train_xml_dir = os.path.join(label_dir, "train")
    train_json = os.path.join(annotations_dir, "train.json")
    xml_to_coco(train_xml_dir, train_json)

    # 转换验证集
    val_xml_dir = os.path.join(label_dir, "val")
    val_json = os.path.join(annotations_dir, "val.json")
    xml_to_coco(val_xml_dir, val_json)

if __name__ == "__main__":
    main()