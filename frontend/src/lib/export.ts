"use client";

import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

/**
 * Client-side CSV export utility.
 * Converts an array of objects into a CSV blob and triggers download.
 */
export function downloadCSV<T extends Record<string, unknown>>(
  rows: T[],
  columns: { key: keyof T; label: string }[],
  filename: string
) {
  if (rows.length === 0) return;

  const header = columns.map((c) => `"${c.label}"`).join(",");
  const body = rows
    .map((row) =>
      columns
        .map((c) => {
          const val = row[c.key];
          if (val === null || val === undefined) return "";
          const s = String(val).replace(/"/g, '""');
          return `"${s}"`;
        })
        .join(",")
    )
    .join("\n");

  const csv = `${header}\n${body}`;
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

/**
 * Client-side PDF export utility.
 * Generates a PDF table from data and triggers download.
 */
export function downloadPDF<T extends Record<string, unknown>>(
  rows: T[],
  columns: { key: keyof T; label: string }[],
  filename: string,
  title?: string
) {
  if (rows.length === 0) return;

  const doc = new jsPDF({ orientation: rows[0] && columns.length > 5 ? "landscape" : "portrait" });

  // Title
  if (title) {
    doc.setFontSize(16);
    doc.setFont("helvetica", "bold");
    doc.text(title, 14, 18);
    doc.setFontSize(9);
    doc.setFont("helvetica", "normal");
    doc.text(`Generated ${new Date().toLocaleDateString()} — ${rows.length} records`, 14, 25);
  }

  const head = [columns.map((c) => c.label)];
  const body = rows.map((row) =>
    columns.map((c) => {
      const val = row[c.key];
      return val === null || val === undefined ? "" : String(val);
    })
  );

  autoTable(doc, {
    head,
    body,
    startY: title ? 30 : 14,
    styles: { fontSize: 8, cellPadding: 2 },
    headStyles: { fillColor: [0, 56, 168], textColor: 255, fontStyle: "bold" },
    alternateRowStyles: { fillColor: [245, 247, 250] },
    margin: { left: 14, right: 14 },
  });

  doc.save(filename);
}
