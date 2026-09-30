export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === "/health") return new Response(JSON.stringify({ status: "HEALTHY", service: "Bio-Robotics Kinematics Core" }), { headers: { "Content-Type": "application/json" } });
    if (url.pathname === "/sse") return new Response("Bio-Robotics Kinematics Core SSE Active", { headers: { "Content-Type": "text/event-stream" } });
    try { return await env.ASSETS.fetch(request); } catch { return new Response("Bio-Robotics Kinematics Core Edge Active"); }
  }
};