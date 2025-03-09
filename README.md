# Simple calendar for my Japanese Learning

This is a simple backendless react page which holds a github actions-coded calendar which will replace / improve upon what I do physically on paper.

At the moment, I write down on a piece of paper what I've done for the day so I can remember - but I think a digital version that I can look at online will be more epic >:&#41;

![Example Image](./src/assets/example_image.jpg)

## ToDo

- [x] figure out how to work the [react-calendar-heatmap](https://github.com/kevinsqi/react-calendar-heatmap)
- [x] simple ~~bash~~ python script to automate updating the json file
- [x] add extra data (what i've done for the day) on ~~click~~ hover
- [ ] more meaningful information on hover
- [ ] figure out this readme situation
- [x] bugfix the tooltip on empty days
- [ ] bonus color for days where i've done additional study (possibly include a note on what i actually did, i'm thinking that gold is a yummy color)
- [ ] format dates on tool tips to be "March 5th" vs "2025-03-05"
- [ ] change data type for data to be more concise i don't think i need the additional tab based on the reformed usage
- [ ] color gradient for css instead of fixed values because i'm limited by my brain
- [ ] tidy and refactor extra hover info :>!
- [ ] due to the chronological nature of how i'm storing the data, possibly use indexes (O(1)) instead of iterating (O(n)) for efficiency
