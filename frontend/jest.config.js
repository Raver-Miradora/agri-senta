/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  testEnvironment: "jsdom",
  setupFilesAfterEnv: ["<rootDir>/jest.setup.ts"],
  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/src/$1",
    "^lucide-react$": "<rootDir>/src/__mocks__/lucide-react.ts",
  },
  transform: {
    "^.+\\.tsx?$": [
      "ts-jest",
      {
        tsconfig: "tsconfig.jest.json",
        jsx: "react-jsx",
        diagnostics: false,
      },
    ],
  },
  testMatch: ["<rootDir>/src/**/*.test.{ts,tsx}"],
  moduleFileExtensions: ["ts", "tsx", "js", "jsx", "json"],
};
