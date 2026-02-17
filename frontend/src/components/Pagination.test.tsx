import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import Pagination from "./Pagination";

describe("Pagination", () => {
  const onPageChange = jest.fn();

  beforeEach(() => {
    onPageChange.mockClear();
  });

  it("renders nothing when totalPages is 1", () => {
    const { container } = render(
      <Pagination currentPage={1} totalPages={1} onPageChange={onPageChange} />
    );
    expect(container.firstChild).toBeNull();
  });

  it("renders page info with current page and total", () => {
    render(
      <Pagination currentPage={2} totalPages={5} onPageChange={onPageChange} />
    );
    expect(screen.getByText(/Page/)).toBeInTheDocument();
    expect(screen.getByLabelText("Page navigation")).toBeInTheDocument();
  });

  it("disables first/previous buttons on page 1", () => {
    render(
      <Pagination currentPage={1} totalPages={5} onPageChange={onPageChange} />
    );
    expect(screen.getByLabelText("First page")).toBeDisabled();
    expect(screen.getByLabelText("Previous page")).toBeDisabled();
  });

  it("disables next/last buttons on last page", () => {
    render(
      <Pagination currentPage={5} totalPages={5} onPageChange={onPageChange} />
    );
    expect(screen.getByLabelText("Last page")).toBeDisabled();
    expect(screen.getByLabelText("Next page")).toBeDisabled();
  });

  it("calls onPageChange when a page button is clicked", () => {
    render(
      <Pagination currentPage={1} totalPages={5} onPageChange={onPageChange} />
    );
    fireEvent.click(screen.getByText("3"));
    expect(onPageChange).toHaveBeenCalledWith(3);
  });

  it("calls onPageChange with next page on next click", () => {
    render(
      <Pagination currentPage={2} totalPages={5} onPageChange={onPageChange} />
    );
    fireEvent.click(screen.getByLabelText("Next page"));
    expect(onPageChange).toHaveBeenCalledWith(3);
  });

  it("calls onPageChange with 1 on first page click", () => {
    render(
      <Pagination currentPage={3} totalPages={5} onPageChange={onPageChange} />
    );
    fireEvent.click(screen.getByLabelText("First page"));
    expect(onPageChange).toHaveBeenCalledWith(1);
  });

  it("has correct aria-label on nav", () => {
    render(
      <Pagination currentPage={1} totalPages={3} onPageChange={onPageChange} />
    );
    expect(screen.getByRole("navigation")).toHaveAttribute(
      "aria-label",
      "Page navigation"
    );
  });
});
