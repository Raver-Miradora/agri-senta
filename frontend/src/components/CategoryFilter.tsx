"use client";

type CategoryFilterProps = {
  categories: string[];
  selected: string;
  onChange: (category: string) => void;
};

export default function CategoryFilter({ categories, selected, onChange }: CategoryFilterProps) {
  return (
    <div className="category-filter" role="tablist" aria-label="Filter by category">
      <button
        className={`category-chip${selected === "All" ? " active" : ""}`}
        onClick={() => onChange("All")}
        role="tab"
        aria-selected={selected === "All"}
      >
        All
      </button>
      {categories.map((cat) => (
        <button
          key={cat}
          className={`category-chip${selected === cat ? " active" : ""}`}
          onClick={() => onChange(cat)}
          role="tab"
          aria-selected={selected === cat}
        >
          {cat}
        </button>
      ))}
    </div>
  );
}
