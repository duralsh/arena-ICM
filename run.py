#!/usr/bin/env python3
"""
Token Economics Calculator for ICO/Presale with GUI

Interactive calculator with sliders to adjust:
- Team allocation percentage (0-30%)
- Funds to raise ($10K-$2M)
- Public sale percentage (0-100%)
- LP percentage (auto-calculated as: LP = 100 - Team - Public)

20% of raised funds allocated to LP.
"""

import tkinter as tk
from tkinter import ttk


class TokenEconomicsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Token Economics Calculator")
        self.root.geometry("950x850")
        self.root.configure(bg='#1e1e1e')
        
        # Constants
        self.TOTAL_SUPPLY = 10_000_000_000  # 10 billion
        self.LP_FUND_PERCENT = 0.20  # 20% of funds go to LP
        
        # Create main frame
        main_frame = tk.Frame(root, bg='#1e1e1e', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(main_frame, text="🚀 Token Economics Calculator", 
                        font=('Arial', 24, 'bold'), bg='#1e1e1e', fg='#00ff88')
        title.pack(pady=(0, 30))
        
        # Control Panel
        controls_frame = tk.Frame(main_frame, bg='#2d2d2d', padx=20, pady=20)
        controls_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Create variables
        self.team_var = tk.DoubleVar(value=10)
        self.funds_var = tk.DoubleVar(value=100_000)
        self.public_var = tk.DoubleVar(value=70)
        
        # Team Token Allocation Slider
        self.create_slider(controls_frame, "Team Token Allocation (%)", 
                          0, 30, 10, self.team_var, 0)
        
        # Funds to Raise Slider
        self.create_slider(controls_frame, "Funds to Raise ($)", 
                          10_000, 2_000_000, 100_000, 
                          self.funds_var, 1,
                          format_value=self.format_currency)
        
        # Public Sale Token Allocation Slider
        self.create_slider(controls_frame, "Public Sale Token Alloc (%)", 
                          0, 100, 70, self.public_var, 2)
        
        # LP Allocation Display (Read-only)
        lp_frame = tk.Frame(controls_frame, bg='#2d2d2d')
        lp_frame.grid(row=3, column=0, columnspan=2, sticky='ew', pady=15)
        
        lp_label = tk.Label(lp_frame, text="LP Alloc (%)", 
                           font=('Arial', 12, 'bold'), bg='#2d2d2d', fg='#ffffff')
        lp_label.pack(anchor='w')
        
        self.lp_value_label = tk.Label(lp_frame, text="20.0%", 
                                       font=('Arial', 16), bg='#2d2d2d', fg='#00ff88')
        self.lp_value_label.pack(anchor='w', pady=(5, 0))
        
        self.lp_bar = ttk.Progressbar(lp_frame, length=400, mode='determinate', 
                                      maximum=100, style='LP.Horizontal.TProgressbar')
        self.lp_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Results Panel with Canvas for scrolling
        results_container = tk.Frame(main_frame, bg='#2d2d2d')
        results_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(results_container, bg='#2d2d2d', highlightthickness=0)
        scrollbar = tk.Scrollbar(results_container, orient="vertical", command=canvas.yview)
        results_frame = tk.Frame(canvas, bg='#2d2d2d', padx=20, pady=20)
        
        results_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=results_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        results_title = tk.Label(results_frame, text="📊 Token Distribution & Valuation", 
                                font=('Arial', 16, 'bold'), bg='#2d2d2d', fg='#00ff88')
        results_title.pack(pady=(0, 10))
        
        # Warning label for invalid allocation
        self.warning_label = tk.Label(results_frame, text="", 
                                     font=('Arial', 12, 'bold'), bg='#2d2d2d', fg='#ff0000')
        self.warning_label.pack(pady=(0, 10))
        
        # Create result labels
        self.result_labels = {}
        result_fields = [
            ("Team Tokens", "team_tokens"),
            ("Public Sale Tokens", "public_tokens"),
            ("LP Tokens", "lp_tokens"),
            ("Total Allocation %", "total_percent"),
            ("", "divider1"),
            ("Total Funds Raised", "total_funds"),
            ("LP Funds (20%)", "lp_funds"),
            ("Team Funds (80%)", "team_funds"),
            ("", "divider2"),
            ("Pre-Market FDV (ICO Price)", "fdv_ico"),
            ("Market FDV (LP Price)", "fdv_lp"),
            ("FDV Multiple", "fdv_multiple"),
        ]
        
        for label_text, key in result_fields:
            if key.startswith("divider"):
                separator = tk.Frame(results_frame, height=2, bg='#444444')
                separator.pack(fill=tk.X, pady=10)
            else:
                self.create_result_row(results_frame, label_text, key)
        
        # Configure progress bar style
        style = ttk.Style()
        style.theme_use('default')
        style.configure('LP.Horizontal.TProgressbar', 
                       background='#00ff88', 
                       troughcolor='#1e1e1e',
                       bordercolor='#2d2d2d',
                       lightcolor='#00ff88',
                       darkcolor='#00ff88')
        
        # Store previous valid values for validation
        self.prev_team = self.team_var.get()
        self.prev_public = self.public_var.get()
        
        # Bind updates with validation and store trace IDs
        self.team_trace_id = self.team_var.trace_add('write', lambda *args: self.validate_and_update('team'))
        self.funds_trace_id = self.funds_var.trace_add('write', lambda *args: self.update_calculations())
        self.public_trace_id = self.public_var.trace_add('write', lambda *args: self.validate_and_update('public'))
        
        # Initial calculation
        self.update_calculations()
    
    def create_slider(self, parent, label_text, from_, to, initial, variable, row, format_value=None):
        frame = tk.Frame(parent, bg='#2d2d2d')
        frame.grid(row=row, column=0, columnspan=2, sticky='ew', pady=15)
        
        label = tk.Label(frame, text=label_text, font=('Arial', 12, 'bold'), 
                        bg='#2d2d2d', fg='#ffffff')
        label.pack(anchor='w')
        
        value_label = tk.Label(frame, text=self.format_value_with_func(initial, format_value), 
                              font=('Arial', 16), bg='#2d2d2d', fg='#00ff88')
        value_label.pack(anchor='w', pady=(5, 0))
        
        if to - from_ <= 2_000_000:
            resolution = 10_000 if to > 100 else 1
        else:
            resolution = 10_000
            
        slider = tk.Scale(frame, from_=from_, to=to, orient=tk.HORIZONTAL,
                         variable=variable, resolution=resolution,
                         bg='#2d2d2d', fg='#ffffff', highlightthickness=0,
                         troughcolor='#1e1e1e', activebackground='#00ff88',
                         length=400, showvalue=0)
        slider.pack(fill=tk.X, pady=(10, 0))
        
        # Update value label when slider moves
        def update_label(*args):
            value_label.config(text=self.format_value_with_func(variable.get(), format_value))
        
        variable.trace_add('write', update_label)
    
    def format_value_with_func(self, value, format_func):
        if format_func:
            return format_func(value)
        return f"{value:.1f}%"
    
    def format_currency(self, value):
        return f"${self.format_number(value)}"
    
    def create_result_row(self, parent, label_text, key):
        frame = tk.Frame(parent, bg='#2d2d2d')
        frame.pack(fill=tk.X, pady=5)
        
        label = tk.Label(frame, text=label_text, font=('Arial', 11), 
                        bg='#2d2d2d', fg='#cccccc', anchor='w')
        label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        value_label = tk.Label(frame, text="...", font=('Arial', 11, 'bold'), 
                              bg='#2d2d2d', fg='#ffffff', anchor='e')
        value_label.pack(side=tk.RIGHT)
        
        self.result_labels[key] = value_label
    
    def format_number(self, num):
        """Format large numbers with commas."""
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:,.2f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:,.2f}M"
        elif num >= 1_000:
            return f"{num / 1_000:,.2f}K"
        else:
            return f"{num:,.2f}"
    
    def validate_and_update(self, slider_type):
        """Validate that team + public < 100, LP > 0, and LP FDV >= ICO FDV before allowing update"""
        team_val = self.team_var.get()
        public_val = self.public_var.get()
        lp_val = 100 - team_val - public_val
        
        is_valid = True
        
        # Check if LP would be negative or zero
        if team_val + public_val >= 100:
            is_valid = False
        
        # Check if LP is too small (must be at least 0.1%)
        elif lp_val < 0.1:
            is_valid = False
        
        # Check if LP FDV would drop below ICO FDV
        # For LP FDV >= ICO FDV, we need: lp_tokens <= 0.2 * public_tokens
        # Which means: lp_percent <= 0.2 * public_percent
        # Also handle edge case where public is very small
        elif public_val > 0.1 and lp_val > 0.2 * public_val:
            is_valid = False
        
        # If invalid, immediately revert without updating display
        if not is_valid:
            # Temporarily disable trace to avoid recursive calls
            self.team_var.trace_remove('write', self.team_trace_id)
            self.public_var.trace_remove('write', self.public_trace_id)
            
            # Revert to previous valid value
            if slider_type == 'team':
                self.team_var.set(self.prev_team)
            elif slider_type == 'public':
                self.public_var.set(self.prev_public)
            
            # Re-enable traces
            self.team_trace_id = self.team_var.trace_add('write', lambda *args: self.validate_and_update('team'))
            self.public_trace_id = self.public_var.trace_add('write', lambda *args: self.validate_and_update('public'))
            return
        
        # Update previous values if valid
        self.prev_team = team_val
        self.prev_public = public_val
        
        # Proceed with calculation
        self.update_calculations()
    
    def update_calculations(self):
        try:
            # Get values
            team_percent = self.team_var.get()
            public_percent = self.public_var.get()
            funds_to_raise = self.funds_var.get()
            
            # Calculate LP percentage: LP = 100 - Team - Public
            lp_percent = 100 - team_percent - public_percent
            
            # Calculate total allocation (should always be 100 unless negative)
            total_percent = team_percent + public_percent + lp_percent
            
            # Calculate token allocations based on percentages
            team_tokens = self.TOTAL_SUPPLY * (team_percent / 100)
            public_tokens = self.TOTAL_SUPPLY * (public_percent / 100)
            lp_tokens = self.TOTAL_SUPPLY * (lp_percent / 100)
            
            # Update LP display (should never be negative or zero due to validation)
            # Check if we're at or very close to a constraint limit
            at_minimum = False
            warning_msg = ""
            
            # Check if LP is very small (close to 0)
            if lp_percent < 1.0:
                at_minimum = True
                warning_msg = "⚠️ At MINIMUM: LP cannot be 0% (slider blocked)"
            # Check if we're at the LP FDV constraint limit
            elif public_percent > 0.1:
                max_lp_allowed = 0.2 * public_percent
                if abs(lp_percent - max_lp_allowed) < 0.5:  # Within 0.5% of limit
                    at_minimum = True
                    warning_msg = "⚠️ At MINIMUM constraint: LP FDV = ICO FDV (slider blocked)"
            
            if at_minimum:
                self.lp_value_label.config(text=f"{lp_percent:.1f}% ⚠️", fg='#ffaa00')
                self.warning_label.config(text=warning_msg)
            else:
                self.lp_value_label.config(text=f"{lp_percent:.1f}%", fg='#00ff88')
                self.warning_label.config(text="")
            self.lp_bar['value'] = max(0, lp_percent)
            
            # Calculate funds distribution
            lp_funds = funds_to_raise * self.LP_FUND_PERCENT
            team_funds = funds_to_raise * (1 - self.LP_FUND_PERCENT)
            
            # Calculate prices
            if public_tokens > 0:
                ico_price = funds_to_raise / public_tokens
            else:
                ico_price = 0
            
            if lp_tokens > 0:
                lp_price = lp_funds / lp_tokens
            else:
                lp_price = 0
            
            # Calculate FDVs
            fdv_ico = self.TOTAL_SUPPLY * ico_price
            fdv_lp = self.TOTAL_SUPPLY * lp_price
            
            # Calculate multiple
            if fdv_ico > 0:
                fdv_multiple = fdv_lp / fdv_ico
            else:
                fdv_multiple = 0
            
            # Update result labels with white text
            self.result_labels['team_tokens'].config(text=f"{self.format_number(team_tokens)} tokens", fg='#ffffff')
            self.result_labels['public_tokens'].config(text=f"{self.format_number(public_tokens)} tokens", fg='#ffffff')
            self.result_labels['lp_tokens'].config(text=f"{self.format_number(lp_tokens)} tokens", fg='#ffffff')
            self.result_labels['total_percent'].config(text="100.0%", fg='#00ff88')
            
            self.result_labels['total_funds'].config(text=f"${self.format_number(funds_to_raise)}", fg='#ffffff')
            self.result_labels['lp_funds'].config(text=f"${self.format_number(lp_funds)}", fg='#ffffff')
            self.result_labels['team_funds'].config(text=f"${self.format_number(team_funds)}", fg='#ffffff')
            
            self.result_labels['fdv_ico'].config(text=f"${self.format_number(fdv_ico)}", fg='#00ff88')
            self.result_labels['fdv_lp'].config(text=f"${self.format_number(fdv_lp)}", fg='#00ff88')
            self.result_labels['fdv_multiple'].config(text=f"{fdv_multiple:.2f}x", fg='#ffffff')
            
            # Debug print
            fdv_ratio = fdv_lp / fdv_ico if fdv_ico > 0 else 0
            print(f"Team: {team_percent}%, Public: {public_percent}%, LP: {lp_percent}%, Total: 100%, FDV_ICO: ${fdv_ico:,.0f}, FDV_LP: ${fdv_lp:,.0f}, Ratio: {fdv_ratio:.2f}x")
            
        except Exception as e:
            print(f"Error in calculations: {e}")


def main():
    root = tk.Tk()
    app = TokenEconomicsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
