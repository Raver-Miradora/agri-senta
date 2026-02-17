import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import CategoryFilter from "./CategoryFilter";

describe("CategoryFilter", () => {
  const categories = ["Rice", "Vegetables", "Meat"];
  const onChange = jest.fn();

  beforeEach(() => {
    onChange.mockClear();
  });

  it("renders 'All' button plus each category", () => {
    render(
      <CategoryFilter categories={categories} selected="All" onChange={onChange} />
    );
    expect(screen.getByText("All")).toBeInTheDocument();
    expect(screen.getByText("Rice")).toBeInTheDocument();
    expect(screen.getByText("Vegetables")).toBeInTheDocument();
    expect(screen.getByText("Meat")).toBeInTheDocument();
  });

  it("marks the selected category with aria-selected", () => {
    render(
      <CategoryFilter categories={categories} selected="Rice" onChange={onChange} />
    );
    expect(screen.getByText("Rice")).toHaveAttribute("aria-selected", "true");
    expect(screen.getByText("All")).toHaveAttribute("aria-selected", "false");
    expect(screen.getByText("Meat")).toHaveAttribute("aria-selected", "false");
  });

  it("calls onChange when a category is clicked", () => {
    render(
      <CategoryFilter categories={categories} selected="All" onChange={onChange} />
    );
    fireEvent.click(screen.getByText("Vegetables"));
    expect(onChange).toHaveBeenCalledWith("Vegetables");
  });

  it("calls onChange with 'All' when All is clicked", () => {
    render(
      <CategoryFilter categories={categories} selected="Rice" onChange={onChange} />
    );
    fireEvent.click(screen.getByText("All"));
    expect(onChange).toHaveBeenCalledWith("All");
  });

  it("has tablist role on container", () => {
    render(
      <CategoryFilter categories={categories} selected="All" onChange={onChange} />
    );
    expect(screen.getByRole("tablist")).toBeInTheDocument();
  });

  it("all buttons have role=tab", () => {
    render(
      <CategoryFilter categories={categories} selected="All" onChange={onChange} />
    );
    const tabs = screen.getAllByRole("tab");
    // All + 3 categories = 4 tabs
    expect(tabs).toHaveLength(4);
  });
});
