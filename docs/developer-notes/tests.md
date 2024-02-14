# Tests

## Integration

```mermaid
---
title: Generating the test data
---
stateDiagram-v2
state Tags {
  generate_tags: Generate tags
  state generate_tags {
    add_tags: Add tags
    add_attributes: Add attributes

    add_attributes --> add_tags
  }

  test_tag_category: Test tag category

  generate_tags --> test_tag_category

  generate_front_tag_settings: Generate front tag settings
  state generate_front_tag_settings {
    add_gallery_categories: Add gallery categories
    add_gallery_tag_fields: Add gallery tag fields
    add_video_categories: Add video categories
    add_video_tag_fields: Add video tag fields
  }

  generate_tags --> generate_front_tag_settings
}

generate_data: Generate data
state generate_data {
  generate_galleries: Generate galleries
  generate_videos: Generate videos
}

Tags --> generate_data

add_storages: Add storages
generate_data --> add_storages
add_storages --> Synchronize

test_sources: Test gallery and video tags
state test_sources {
  crud_sources: CRUD gallery and video tags
  search
}

delete_sources: Delete gallery and video tags
modify_gallery_tags_locally: Modify gallery tags locally

Synchronize --> test_sources
Synchronize --> modify_gallery_tags_locally
modify_gallery_tags_locally --> Synchronize

test_sources --> delete_sources
delete_sources --> Synchronize

generate_standalone_data: Generate standalone data
test_standalone_commands: Test standalone commands
generate_standalone_data --> test_standalone_commands
Synchronize --> generate_standalone_data

test_standalone_commands --> test_sources
```

## Search

## Pagination

Here are the scenarios when we use pagination.

- Gallery previews
  - Default
  - Search
  - Advanced search
- Preview images in gallery
- Video previews
- Bookmark
- CRUD table

## Gallery

### Synchronize

- If the JSON file in the gallery is different from the document in Elasticsearch, we
  should base on the JSON file and update the document in Elasticsearch.
- If the gallery is deleted from storage, the document must also be deleted from
  Elasticsearch.
