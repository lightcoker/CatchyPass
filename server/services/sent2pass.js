module.exports = (
  sentences,
  keywords,
  delimiter = "",
  toLeet = true,
  wordIndex = -1,
  lineIndexes = [0, 1, 4]
) => {
  const REGEX = /[-!$%^&*()_+|~=`{}[:;<>?,.@#\]]/g;
  const LEET_DICT = {
    a: 4,
    b: 8,
    e: 3,
    g: 6,
    l: 1,
    o: 0,
    r: 2,
    s: 5,
    t: 7,
    z: 2,
  };

  const words = sentences
    .split("\n")
    .map((line, index) => {
      if (lineIndexes.includes(index)) return line.replace(REGEX, "");
    })
    .filter((elem) => {
      return typeof elem === "string";
    })
    .map((line) => {
      return line
        .split(" ")
        .filter((word) => word !== "")
        .slice(wordIndex);
    });

  if (toLeet) {
    keywords = keywords.map((keyword) => {
      return keyword
        .toLowerCase()
        .split("")
        .map((c) => {
          if (c in LEET_DICT) return LEET_DICT[c];
          return c;
        })
        .join("");
    });
  }

  return [...keywords, ...words]
    .flat(1)
    .map((word) => {
      return word.charAt(0).toUpperCase() + word.slice(1);
    })
    .join(delimiter);
};
