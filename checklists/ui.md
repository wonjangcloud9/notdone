# UI evidence

Taking the screenshot is not the point. Looking at it is.

## The four shots

**Light.** The default. Check that nothing overflows its container and no text is clipped.

**Dark.** The usual failures are a hardcoded `#fff` background, text at the same lightness as what is behind it, and a border that vanishes. If your CSS defines a color only inside a `prefers-color-scheme` block, the other theme has no value at all.

**Empty.** Zero items, zero results, first run. This is the state a new user sees first and the one that is tested least. A list component with no rows should say something, not collapse to nothing.

**~400px wide.** Phone width. Look for horizontal scroll on the page body, a `min-width` wider than the screen, and rows that should have wrapped.

## What counts as looking

Name the thing you checked, not the file you saved:

> `settings-dark.png` — labels are readable against the panel, the divider is still visible, the toggle keeps its focus ring.

Not:

> Took screenshots of both themes.

## Also worth a shot, when relevant

- **Long content.** A name that is 60 characters. A number with eight digits. Real data is uglier than fixtures.
- **Loading.** If it takes a network call, the intermediate state is part of the UI.
- **Error.** The failure path you wrote is a screen too.
- **Focus.** Tab through it once. An interactive element you cannot reach by keyboard is not finished.
