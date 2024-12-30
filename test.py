import numpy as np
import plotly.graph_objects as go

# ----------------------------------------------------------------
# 1. Increase the resolution for smoother folds
# ----------------------------------------------------------------
n = 150  # Higher resolution
theta_vals = np.linspace(0, 2 * np.pi, n)
phi_vals = np.linspace(0, np.pi, n)
THETA, PHI = np.meshgrid(theta_vals, phi_vals)

# ----------------------------------------------------------------
# 2. Define three folded radii (capabilities) with distinct patterns
# ----------------------------------------------------------------
r1 = 1 + 0.2 * np.sin(3 * PHI) * np.cos(3 * THETA)
r2 = 1 + 0.2 * np.cos(4 * PHI) * np.sin(3 * THETA)
r3 = 1 + 0.2 * np.sin(3 * PHI + 1) * np.sin(4 * THETA + 1)

# Convert spherical -> Cartesian for each "capability" surface
# x = r sin(phi) cos(theta)
# y = r sin(phi) sin(theta)
# z = r cos(phi)

x1 = r1 * np.sin(PHI) * np.cos(THETA)
y1 = r1 * np.sin(PHI) * np.sin(THETA)
z1 = r1 * np.cos(PHI)

x2 = r2 * np.sin(PHI) * np.cos(THETA)
y2 = r2 * np.sin(PHI) * np.sin(THETA)
z2 = r2 * np.cos(PHI)

x3 = r3 * np.sin(PHI) * np.cos(THETA)
y3 = r3 * np.sin(PHI) * np.sin(THETA)
z3 = r3 * np.cos(PHI)

# ----------------------------------------------------------------
# 3. Create 3D surfaces with partial opacity and improved lighting
# ----------------------------------------------------------------
lighting_config = dict(
    ambient=0.4,  # overall ambient light
    diffuse=0.8,
    specular=0.5,
    roughness=0.5,
    fresnel=0.2,
)

surface1 = go.Surface(
    x=x1,
    y=y1,
    z=z1,
    surfacecolor=r1,
    name="Capability 1",
    colorscale=[[0, "white"], [1, "red"]],
    opacity=0.6,
    showscale=True,
    colorbar=dict(title="Cap1 (Fold)", len=0.4),
    hovertemplate="Cap1 radius: %{surfacecolor:.2f}",
    lighting=lighting_config,
)

surface2 = go.Surface(
    x=x2,
    y=y2,
    z=z2,
    surfacecolor=r2,
    name="Capability 2",
    colorscale=[[0, "white"], [1, "green"]],
    opacity=0.6,
    showscale=True,
    colorbar=dict(title="Cap2 (Fold)", len=0.4),
    hovertemplate="Cap2 radius: %{surfacecolor:.2f}",
    lighting=lighting_config,
)

surface3 = go.Surface(
    x=x3,
    y=y3,
    z=z3,
    surfacecolor=r3,
    name="Capability 3",
    colorscale=[[0, "white"], [1, "blue"]],
    opacity=0.6,
    showscale=True,
    colorbar=dict(title="Cap3 (Fold)", len=0.4),
    hovertemplate="Cap3 radius: %{surfacecolor:.2f}",
    lighting=lighting_config,
)

# ----------------------------------------------------------------
# 4. Add a semi-transparent outer sphere for boundary
# ----------------------------------------------------------------
shell_radius = 1.3
xshell = shell_radius * np.sin(PHI) * np.cos(THETA)
yshell = shell_radius * np.sin(PHI) * np.sin(THETA)
zshell = shell_radius * np.cos(PHI)

outer_shell = go.Surface(
    x=xshell,
    y=yshell,
    z=zshell,
    surfacecolor=np.zeros_like(xshell),
    colorscale=[[0, "lightgray"], [1, "lightgray"]],
    opacity=0.2,
    name="Model Space Boundary",
    showscale=False,
    hoverinfo="skip",
)

# ----------------------------------------------------------------
# 5. Build the Plotly figure
#    - Add toggles to show/hide surfaces
#    - Adjust camera for a nicer initial angle
# ----------------------------------------------------------------
fig = go.Figure(data=[surface1, surface2, surface3, outer_shell])

# Create toggle buttons so you can show/hide each capability surface
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            x=0.7,
            y=1.15,
            buttons=[
                dict(
                    label="Toggle Cap1",
                    method="update",
                    args=[
                        {"visible": [True, None, None, True]},  # Cap1 toggles
                        {},  # layout changes
                    ],
                ),
                dict(
                    label="Toggle Cap2",
                    method="update",
                    args=[{"visible": [None, True, None, True]}, {}],  # Cap2 toggles
                ),
                dict(
                    label="Toggle Cap3",
                    method="update",
                    args=[{"visible": [None, None, True, True]}, {}],  # Cap3 toggles
                ),
            ],
        )
    ],
    title="Neuromosaic 3D High‐Fidelity Visualization",
    scene=dict(
        xaxis_title="X",
        yaxis_title="Y",
        zaxis_title="Z",
        aspectmode="cube",
        camera=dict(
            eye=dict(x=1.2, y=1.2, z=1.1),  # Adjust to taste
        ),
    ),
)

fig.show()
