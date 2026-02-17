// Mock all lucide-react icons as simple span elements
const createMockIcon = (name: string) => {
  const MockIcon = (props: React.SVGAttributes<SVGElement>) => {
    const React = require("react");
    return React.createElement("span", { "data-testid": `icon-${name}`, ...props });
  };
  MockIcon.displayName = name;
  return MockIcon;
};

module.exports = new Proxy(
  {},
  {
    get: (_target, prop: string) => createMockIcon(prop),
  }
);
