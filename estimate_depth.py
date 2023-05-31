import argparse
import torch
from PIL import Image
from pathlib import Path
from zoedepth.utils.misc import pil_to_batched_tensor, get_image_from_url, save_raw_16bit, colorize

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def main():
    parser = argparse.ArgumentParser(description="ZoeDepth - Depth Estimation")
    parser.add_argument("-i", "--input", type=str, help="Path to the input image file or URL")
    parser.add_argument("-o", "--output", type=str, help="Path to save the output depth image")
    parser.add_argument("-c", "--with-colored-output", action="store_true", help="Enable colored output")
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    #zoe = torch.hub.load("isl-org/ZoeDepth", "ZoeD_NK", pretrained=True).to(DEVICE).eval()
    zoe = torch.hub.load("isl-org/ZoeDepth", "ZoeD_N", pretrained=True).to(DEVICE).eval()

    if args.input.startswith("http://") or args.input.startswith("https://"):
        image = get_image_from_url(args.input)
    else:
        image = Image.open(args.input).convert("RGB")

    x = pil_to_batched_tensor(image).to(device)
    depth_tensor = zoe.infer(x)
    depth = depth_tensor.detach().to("cpu").squeeze().numpy()

    save_raw_16bit(depth, args.output)
    if args.with_colored_output:
        colored = colorize(depth, cmap="magma_r")
        #colored = colorize(depth, cmap="magma_r")
        output_path = args.output
        output_dir_path = str(Path(output_path).parent)
        output_image_name_stem = Path(output_path).stem
        output_image_suffix = Path(output_path).suffix
        colored_output_path = str(Path(output_dir_path, output_image_name_stem + "_colored" + output_image_suffix))
        Image.fromarray(colored).save(colored_output_path)
        print(f"colorized depth image saved to {colored_output_path}")


if __name__ == "__main__":
    main()
