document.addEventListener("DOMContentLoaded", () => {
  const splitIntoParagraphs = (text, sentencesPerParagraph) => {
    const clean = text.replace(/\s+/g, " ").trim();
    if (!clean) {
      return [];
    }

    const sentences = clean.split(/(?<=[.!?])\s+/).filter(Boolean);
    if (sentences.length <= sentencesPerParagraph) {
      return [clean];
    }

    const output = [];
    for (let i = 0; i < sentences.length; i += sentencesPerParagraph) {
      const chunk = sentences.slice(i, i + sentencesPerParagraph).join(" ").trim();
      if (chunk) {
        output.push(chunk);
      }
    }

    return output;
  };

  const paragraphizeBlocks = () => {
    const blocks = document.querySelectorAll(".js-paragraphize");
    blocks.forEach((block) => {
      const paragraphs = block.querySelectorAll("p");
      if (paragraphs.length !== 1) {
        return;
      }

      const onlyParagraph = paragraphs[0];
      const original = onlyParagraph.textContent || "";
      if (original.trim().length < 460) {
        return;
      }

      const newParagraphs = splitIntoParagraphs(original, 2);
      if (newParagraphs.length <= 1) {
        return;
      }

      onlyParagraph.remove();
      newParagraphs.forEach((text) => {
        const p = document.createElement("p");
        p.textContent = text;
        block.appendChild(p);
      });
    });
  };

  paragraphizeBlocks();

  const revealItems = Array.from(document.querySelectorAll(".reveal"));

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );

    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  }

  const searchForm = document.querySelector(".search-form");
  if (searchForm) {
    searchForm.addEventListener("submit", () => {
      const submitButton = searchForm.querySelector("button[type='submit']");
      if (!submitButton) {
        return;
      }

      submitButton.disabled = true;
      submitButton.textContent = "Processando...";
      submitButton.classList.add("is-loading");
    });
  }
});
