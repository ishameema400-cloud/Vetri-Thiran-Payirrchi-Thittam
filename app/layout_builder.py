def build_comic_layout(image_paths: list, full_story: str, outline: list) -> list:
    """
    Organizes generated images and full comic story into a structured layout list.
    """
    story_panels = full_story.split("**Panel")
    story_panels = [f"**Panel{panel}" for panel in story_panels if panel.strip()]

    if len(story_panels) < len(outline):
        story_panels = [f"**Panel {i+1}**\n{full_story}" for i in range(len(outline))]

    layout = []
    for idx, (image, text, panel_info) in enumerate(zip(image_paths, story_panels, outline), start=1):
        lines = text.strip().splitlines()
        content_text = "\n".join(lines[1:]).strip() if len(lines) > 1 else text.strip()

        layout.append({
            "panel": idx,
            "title": panel_info.get("title", f"Panel {idx}"),
            "image_path": image,
            "text": content_text,
            "scene_description": panel_info.get("scene_description", ""),
            "image_prompt": panel_info.get("image_prompt", "")
        })

    return layout