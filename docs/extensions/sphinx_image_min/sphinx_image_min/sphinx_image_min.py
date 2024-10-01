"""
Xsolla Sphinx Extension: sphinx_image_min
- Optimizes images in the build/_images directory using Pillow
"""

import os
from sphinx.util.docutils import SphinxDirective
from PIL import Image


class SphinxImageMin(SphinxDirective):
    """Directive to trigger image optimization after Sphinx build."""

    # This directive doesn't insert any nodes in the document
    # It serves as a placeholder for potential future extensions

    def run(self):
        return []


def optimize_images(app, exception):
    """Optimize images using Pillow when building on Read the Docs."""
    # Check if the image optimization is enabled
    if not app.config.img_optimization_enabled:
        print("[sphinx_image_min] Image optimization is disabled. Skipping...")
        return

    if app.builder.name != "html" or exception is not None:
        return

    # Get the maximum width from the configuration
    max_width = app.config.img_optimization_max_width

    # Directory for images output
    try:
        images_dir = os.path.join(app.outdir, "_images")  # Build _images output
        optimize_images_with_pillow(images_dir, max_width)
        print(f"[sphinx_image_min] Image optimization completed.")
    except Exception as e:
        print(f"[sphinx_image_min] Error during image optimization: {e}")


def optimize_images_with_pillow(directory, max_width):
    """Optimize all PNG and JPEG images in the given directory using Pillow."""
    print(f"\n[sphinx_image_min] Starting image optimization in '{directory}'...")
    for filename in os.listdir(directory):
        if filename.lower().endswith(
            (".png", ".jpg", ".jpeg")
        ):  # Handle both PNG and JPEG
            file_path = os.path.join(directory, filename)
            try:
                with Image.open(file_path) as img:
                    # Resize image if it's wider than max_width
                    if img.width > max_width:
                        ratio = max_width / float(img.width)
                        new_height = int((float(img.height) * float(ratio)))
                        img = img.resize(
                            (max_width, new_height), Image.Resampling.LANCZOS
                        )  # HD downsampling

                    # Convert to RGB if not already in RGB mode
                    if img.mode in ("RGBA", "LA") or (
                        img.mode == "P" and "transparency" in img.info
                    ):
                        img = img.convert("RGBA")
                    elif img.mode != "RGB":
                        img = img.convert("RGB")

                    # Optimize image
                    img.save(
                        file_path, optimize=True, quality=85
                    )  # Optimize with a quality setting for JPEG
                print(f"Optimized {filename} using Pillow")
            except Exception as e:
                print(f"Error optimizing {filename}: {e}")
