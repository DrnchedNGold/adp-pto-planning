// frontend/src/components/DonutChart.tsx
import React, { useState } from "react";

type DonutChartSection = {
  value: number;
  color: string;
};

type DonutChartProps = {
  sections: DonutChartSection[];
  total: number;
  size?: number;
  defaultText?: string | number;  
};

export function DonutChart({ sections, total, size = 200, defaultText }: DonutChartProps) {
  const [hovered, setHovered] = useState<number | null>(null);

  const padding = 20; // extra space so expanded slices aren’t clipped
  const viewBoxSize = size + padding * 2;
  const center = viewBoxSize / 2;

  const innerRadius = size * 0.42; // thin ring
  const outerRadius = size * 0.48;
  const expandedOuterRadius = size * 0.52; // a bit further, needs padding

  const totalValue = sections.reduce((acc, s) => acc + s.value, 0);
  let acc = 0;

  function polarToCartesian(r: number, angle: number) {
    return [center + r * Math.cos(angle), center + r * Math.sin(angle)];
  }

  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${viewBoxSize} ${viewBoxSize}`}
    >
      {sections.map((section, i) => {
        const startAngle = (acc / totalValue) * 2 * Math.PI - Math.PI / 2;
        const endAngle =
          ((acc + section.value) / totalValue) * 2 * Math.PI - Math.PI / 2;
        const largeArc = endAngle - startAngle > Math.PI ? 1 : 0;

        const outerR = hovered === i ? expandedOuterRadius : outerRadius;

        const [x1, y1] = polarToCartesian(outerR, startAngle);
        const [x2, y2] = polarToCartesian(outerR, endAngle);
        const [x3, y3] = polarToCartesian(innerRadius, endAngle);
        const [x4, y4] = polarToCartesian(innerRadius, startAngle);

        const pathData = [
          `M ${x1} ${y1}`,
          `A ${outerR} ${outerR} 0 ${largeArc} 1 ${x2} ${y2}`,
          `L ${x3} ${y3}`,
          `A ${innerRadius} ${innerRadius} 0 ${largeArc} 0 ${x4} ${y4}`,
          "Z",
        ].join(" ");

        acc += section.value;

        return (
          <path
            key={i}
            d={pathData}
            fill={section.color}
            style={{ cursor: "pointer", transition: "all 0.3s ease" }}
            onMouseEnter={() => setHovered(i)}
            onMouseLeave={() => setHovered(null)}
          />
        );
      })}

      {/* White center circle */}
      <circle cx={center} cy={center} r={innerRadius - 4} fill="#fff" />

      {/* Center text (total or hovered slice) */}
      <text
        x={center}
        y={center}
        textAnchor="middle"
        dominantBaseline="middle"
        fontSize={22}
        fill="#333"
        fontWeight="bold"
      >
        {hovered !== null ? `${sections[hovered].value}/${total}` : defaultText ?? total}
      </text>
    </svg>
  );
}
