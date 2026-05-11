import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

// MetricCards Component - Displays three metric cards
function MetricCards({ fundName, balance, totalContributed, grantsThisYear }) {
  return (
    <>
      <h1 className="text-4xl font-serif text-on-surface text-center mb-3 tracking-widest">
        {fundName}
      </h1>
      <section className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        {/* Card 1: Current Balance - Visually Dominant */}
        <div className="bg-surface-container-lowest p-4 rounded-md border-l-4 border-l-primary border-t border-r border-b border-outline-variant shadow-md hover:shadow-lg transition-all">
          <div className="flex justify-between items-start mb-2">
            <p className="text-sm text-on-surface-variant font-medium">
              Current Balance
            </p>
            <span className="material-symbols-outlined text-primary">
              account_balance_wallet
            </span>
          </div>
          <h2
            className="text-4xl text-on-surface font-extrabold"
            style={{ fontVariantNumeric: "tabular-nums" }}
          >
            $
            {parseFloat(balance).toLocaleString("en-US", {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </h2>
          <p className="mt-1 text-sm text-on-surface-variant">
            Available to grant
          </p>
        </div>

        {/* Card 2: Total Contributed */}
        <div className="bg-surface-container-lowest p-6 rounded-md border border-outline-variant shadow-sm hover:shadow-md transition-all">
          <div className="flex justify-between items-start mb-2">
            <p className="text-sm text-on-surface-variant font-medium">
              Total Contributed
            </p>
            <span className="material-symbols-outlined text-primary">
              volunteer_activism
            </span>
          </div>
          <h2
            className="text-3xl text-on-surface font-extrabold"
            style={{ fontVariantNumeric: "tabular-nums" }}
          >
            $
            {parseFloat(totalContributed).toLocaleString("en-US", {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </h2>
          <div className="mt-1 flex items-center gap-1">
            <span className="material-symbols-outlined text-base text-primary">
              trending_up
            </span>
            <p className="text-sm text-on-surface-variant">Lifetime impact</p>
          </div>
        </div>

        {/* Card 3: Grants This Year */}
        <div className="bg-surface-container-lowest p-6 rounded-md border border-outline-variant shadow-sm hover:shadow-md transition-all">
          <div className="flex justify-between items-start mb-2">
            <p className="text-sm text-on-surface-variant font-medium">
              Grants This Year
            </p>
            <span className="material-symbols-outlined text-primary">
              send_money
            </span>
          </div>
          <div className="flex items-baseline gap-1">
            <h2
              className="text-3xl text-on-surface font-extrabold"
              style={{ fontVariantNumeric: "tabular-nums" }}
            >
              $
              {parseFloat(grantsThisYear.total).toLocaleString("en-US", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              })}
            </h2>
            <span className="text-sm text-on-surface-variant">
              / {grantsThisYear.count} Grant
              {grantsThisYear.count !== 1 ? "s" : ""}
            </span>
          </div>
        </div>
      </section>
    </>
  );
}

// BalanceChart Component - Shows fund balance over time
function BalanceChart({ balanceOverTime }) {
  if (!balanceOverTime || balanceOverTime.length === 0) {
    return (
      <div className="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold text-on-surface mb-2">
          Balance Over Time
        </h2>
        <div className="h-64 flex items-center justify-center text-on-surface-variant">
          No data available
        </div>
      </div>
    );
  }

  // Format data for Recharts
  const chartData = balanceOverTime.map((item) => ({
    month: new Date(item.month + "-01").toLocaleDateString("en-US", {
      month: "short",
    }),
    balance: parseFloat(item.balance),
  }));

  // Custom tooltip formatter
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-surface-container-lowest border border-outline-variant rounded-lg p-3 shadow-md">
          <p className="text-sm text-on-surface-variant">
            {payload[0].payload.month}
          </p>
          <p className="text-base font-semibold text-primary">
            $
            {payload[0].value.toLocaleString("en-US", {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 mb-6">
      <h2 className="text-xl font-semibold text-on-surface mb-2">
        Balance Over Time
      </h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart
          data={chartData}
          margin={{ top: 5, right: 20, bottom: 5, left: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(111, 12%, 76%)" />
          <XAxis
            dataKey="month"
            stroke="hsl(120, 7%, 27%)"
            style={{ fontSize: "14px" }}
          />
          <YAxis
            stroke="hsl(120, 7%, 27%)"
            style={{ fontSize: "14px" }}
            tickFormatter={(value) => `$${value.toLocaleString()}`}
          />
          <Tooltip content={<CustomTooltip />} />
          <Line
            type="monotone"
            dataKey="balance"
            stroke="hsl(146, 100%, 20%)"
            strokeWidth={2}
            dot={{ fill: "hsl(146, 100%, 20%)", r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

// RecentGrantsTable Component - Shows recent grant recommendations
function RecentGrantsTable({ recentGrants }) {
  if (!recentGrants || recentGrants.length === 0) {
    return (
      <div className="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-on-surface">
            Recent Grant Recommendations
          </h2>
          <a
            href="/grants/create/"
            className="bg-primary text-on-primary px-4 py-2 rounded-md font-medium hover:bg-primary-container hover:text-on-primary-container transition-colors"
          >
            Recommend a Grant
          </a>
        </div>
        <p className="text-on-surface-variant">No grant recommendations yet</p>
      </div>
    );
  }

  // Status badge component
  const StatusBadge = ({ status }) => {
    const statusConfig = {
      pending: {
        bgClass: "bg-tertiary-container",
        textClass: "text-on-tertiary-container",
        label: "Pending",
      },
      approved: {
        bgClass: "bg-secondary-container",
        textClass: "text-on-secondary-container",
        label: "Approved",
      },
      denied: {
        bgClass: "bg-error-container",
        textClass: "text-on-error-container",
        label: "Denied",
      },
    };

    const config = statusConfig[status] || statusConfig.pending;

    return (
      <span
        className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${config.bgClass} ${config.textClass}`}
      >
        {config.label}
      </span>
    );
  };

  return (
    <div className="bg-surface-container-lowest border border-outline-variant rounded-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-on-surface">
          Recent Grant Recommendations
        </h2>
        <a
          href="/grants/create/"
          className="bg-primary text-on-primary px-4 py-2 rounded-md font-medium hover:bg-primary-container hover:text-on-primary-container transition-colors"
        >
          Recommend a Grant
        </a>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-surface-container text-on-surface-variant text-xs uppercase tracking-wider font-semibold">
              <th className="px-6 py-4">Date</th>
              <th className="px-6 py-4">Nonprofit</th>
              <th className="px-6 py-4">Amount</th>
              <th className="px-6 py-4">Status</th>
              <th className="px-6 py-4">Staff Note</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-outline-variant">
            {recentGrants.map((grant) => (
              <tr
                key={grant.id}
                className="hover:bg-surface-container transition-colors"
              >
                <td className="px-6 py-4 text-sm text-on-surface" style={{ fontVariantNumeric: 'tabular-nums' }}>
                  {grant.created_at
                    ? new Date(grant.created_at).toLocaleDateString("en-US", {
                        year: "numeric",
                        month: "2-digit",
                        day: "2-digit",
                      })
                    : "—"}
                </td>
                <td className="px-6 py-4">
                  <p className="text-sm font-semibold text-on-surface">{grant.nonprofit_name}</p>
                </td>
                <td className="px-6 py-4 text-sm text-on-surface" style={{ fontVariantNumeric: 'tabular-nums' }}>
                  $
                  {parseFloat(grant.amount).toLocaleString("en-US", {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })}
                </td>
                <td className="px-6 py-4">
                  <StatusBadge status={grant.status} />
                </td>
                <td className="px-6 py-4 text-sm text-on-surface-variant italic">
                  {grant.staff_note || "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// Main DonorDashboard Component
export default function DonorDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    // Fetch dashboard data from API
    fetch("/api/dashboard/")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch dashboard data");
        }
        return response.json();
      })
      .then((data) => {
        setData(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Dashboard API error:", err);
        setError(true);
        setLoading(false);
      });
  }, []);

  // Loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-on-surface-variant">Loading dashboard...</div>
      </div>
    );
  }

  // Error state - fail silently with fallback UI
  if (error || !data) {
    return (
      <div className="bg-surface-container-lowest border border-outline-variant rounded-lg p-8">
        <h2 className="text-xl font-semibold text-on-surface mb-2">
          Dashboard
        </h2>
        <p className="text-on-surface-variant">
          Unable to load dashboard data at this time. Please try refreshing the
          page.
        </p>
      </div>
    );
  }

  // Render dashboard with data
  return (
    <div className="max-w-full mx-auto px-2">
      <MetricCards
        fundName={data.fund_name}
        balance={data.balance}
        totalContributed={data.total_contributed}
        grantsThisYear={data.grants_this_year}
      />
      <BalanceChart balanceOverTime={data.balance_over_time} />
      <RecentGrantsTable recentGrants={data.recent_grants} />
    </div>
  );
}
