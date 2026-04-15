package reddit

import "testing"

func TestFilterWallpaperPosts(t *testing.T) {
	posts := []SavedPost{
		{ID: "1", Subreddit: "wallpapers", URL: "https://example.com/1.jpg", Title: "ok"},
		{ID: "2", Subreddit: "wallpaper", URL: "https://example.com/1.jpg", Title: "duplicate"},
		{ID: "3", Subreddit: "wallpapers", URL: "ftp://example.com/2.jpg", Title: "invalid"},
		{ID: "4", Subreddit: "golang", URL: "https://example.com/3.jpg", Title: "wrong sub"},
	}

	filtered := FilterWallpaperPosts(posts)

	if len(filtered) != 1 {
		t.Fatalf("expected 1 post after filtering, got %d", len(filtered))
	}
	if filtered[0].ID != "1" {
		t.Fatalf("expected ID 1, got %s", filtered[0].ID)
	}
}
