# Feature Specification: Full-Stack Web Todo Application

**Feature Branch**: `002-fullstack-web-app`
**Created**: 2025-12-02
**Status**: Draft
**Input**: User description: "Full-Stack Web Todo Application with user authentication, RESTful API, and persistent storage - Transform Phase I console app into a multi-user web application"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration (Priority: P1)

A new user wants to create an account to start managing their personal tasks. They visit the application, provide their email and password, and receive confirmation of successful registration.

**Why this priority**: Without user accounts, the application cannot provide personalized, persistent task management. This is the foundation for all other features.

**Independent Test**: Can be fully tested by completing the registration form and verifying the user can subsequently log in. Delivers the ability to create a personal account.

**Acceptance Scenarios**:

1. **Given** an unregistered user on the registration page, **When** they enter a valid email and password (min 8 characters), **Then** the system creates their account and redirects to the dashboard
2. **Given** a user attempting to register, **When** they enter an email already in use, **Then** the system displays an error message indicating the email is taken
3. **Given** a user attempting to register, **When** they enter a password shorter than 8 characters, **Then** the system displays a validation error

---

### User Story 2 - User Login (Priority: P1)

A registered user wants to access their tasks by logging into their account. They enter their credentials and gain access to their personal dashboard.

**Why this priority**: Users must be able to authenticate to access their tasks. This enables the core value proposition of persistent, personalized task management.

**Independent Test**: Can be fully tested by logging in with valid credentials and verifying access to the dashboard. Delivers secure access to personal data.

**Acceptance Scenarios**:

1. **Given** a registered user on the login page, **When** they enter correct email and password, **Then** the system authenticates them and redirects to their dashboard
2. **Given** a user on the login page, **When** they enter incorrect credentials, **Then** the system displays an authentication error without revealing which field was wrong
3. **Given** an authenticated user, **When** they close and reopen the browser within session validity, **Then** they remain logged in

---

### User Story 3 - View Task List (Priority: P1)

An authenticated user wants to see all their tasks in one place. They access their dashboard and see a list of all their tasks with title, completion status, and creation date.

**Why this priority**: Viewing tasks is the core read operation. Users need to see their tasks before they can manage them.

**Independent Test**: Can be fully tested by logging in and verifying the task list displays correctly. Delivers visibility into all personal tasks.

**Acceptance Scenarios**:

1. **Given** an authenticated user with existing tasks, **When** they access the dashboard, **Then** they see all their tasks listed with title and completion status
2. **Given** an authenticated user with no tasks, **When** they access the dashboard, **Then** they see an empty state message encouraging them to add their first task
3. **Given** an authenticated user, **When** they view the task list, **Then** they only see tasks they created (not other users' tasks)

---

### User Story 4 - Add New Task (Priority: P2)

An authenticated user wants to add a new task to their list. They enter a task title and optionally a description, then save it.

**Why this priority**: Creating tasks is essential for task management, but viewing existing tasks (P1) provides more immediate value for users with existing data.

**Independent Test**: Can be fully tested by adding a new task and verifying it appears in the task list. Delivers the ability to capture new tasks.

**Acceptance Scenarios**:

1. **Given** an authenticated user on the dashboard, **When** they enter a task title (1-200 characters) and submit, **Then** the task is created and appears in their list
2. **Given** an authenticated user creating a task, **When** they add an optional description (up to 1000 characters), **Then** the description is saved with the task
3. **Given** an authenticated user, **When** they attempt to create a task with an empty title, **Then** the system displays a validation error

---

### User Story 5 - Update Task (Priority: P2)

An authenticated user wants to modify an existing task's title or description. They select a task, edit the details, and save the changes.

**Why this priority**: Editing tasks allows users to correct mistakes and update task details as requirements change.

**Independent Test**: Can be fully tested by editing an existing task and verifying the changes persist. Delivers task modification capability.

**Acceptance Scenarios**:

1. **Given** an authenticated user viewing their tasks, **When** they select a task to edit and change the title, **Then** the updated title is saved and displayed
2. **Given** an authenticated user editing a task, **When** they modify the description, **Then** the updated description is saved
3. **Given** an authenticated user, **When** they attempt to update another user's task, **Then** the system denies the action

---

### User Story 6 - Mark Task Complete (Priority: P3)

An authenticated user wants to mark a task as complete or incomplete. They toggle the completion status with a single action.

**Why this priority**: Completion tracking is important but secondary to core CRUD operations.

**Independent Test**: Can be fully tested by toggling task completion and verifying the status change persists. Delivers progress tracking.

**Acceptance Scenarios**:

1. **Given** an authenticated user with an incomplete task, **When** they mark it as complete, **Then** the task displays as completed
2. **Given** an authenticated user with a completed task, **When** they mark it as incomplete, **Then** the task displays as not completed
3. **Given** an authenticated user, **When** they toggle completion, **Then** the change is immediately visible without page refresh

---

### User Story 7 - Delete Task (Priority: P3)

An authenticated user wants to remove a task they no longer need. They select delete and confirm the action.

**Why this priority**: Deletion is important for list hygiene but less critical than creating and managing active tasks.

**Independent Test**: Can be fully tested by deleting a task and verifying it no longer appears in the list. Delivers task removal capability.

**Acceptance Scenarios**:

1. **Given** an authenticated user with a task, **When** they choose to delete it and confirm, **Then** the task is permanently removed from their list
2. **Given** an authenticated user attempting to delete, **When** they cancel the confirmation, **Then** the task remains in their list
3. **Given** an authenticated user, **When** they delete a task, **Then** the deletion is immediate and the list updates

---

### User Story 8 - User Logout (Priority: P4)

An authenticated user wants to securely end their session. They click logout and are returned to the login page.

**Why this priority**: Important for security but not core to task management functionality.

**Independent Test**: Can be fully tested by logging out and verifying session is terminated. Delivers secure session management.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** they click logout, **Then** their session is terminated and they are redirected to the login page
2. **Given** a logged-out user, **When** they attempt to access the dashboard directly, **Then** they are redirected to the login page
3. **Given** a logged-out user, **When** they use the back button after logout, **Then** they cannot access protected content

---

### Edge Cases

- What happens when a user's session expires while they are editing a task? The system should prompt re-authentication and preserve unsaved changes where possible.
- How does the system handle concurrent edits to the same task from multiple browser tabs? Last write wins, with no explicit conflict resolution.
- What happens when a user attempts to access a task that was deleted in another session? The system displays a "task not found" message.
- How does the system handle network connectivity issues during task operations? Display appropriate error messages and allow retry.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to register with email and password
- **FR-002**: System MUST validate email format during registration
- **FR-003**: System MUST enforce minimum password length of 8 characters
- **FR-004**: System MUST authenticate users with email and password
- **FR-005**: System MUST maintain user sessions across browser sessions (within validity period)
- **FR-006**: System MUST display only tasks belonging to the authenticated user
- **FR-007**: System MUST allow creation of tasks with title (1-200 chars) and optional description (max 1000 chars)
- **FR-008**: System MUST allow editing of task title and description
- **FR-009**: System MUST allow toggling task completion status
- **FR-010**: System MUST allow deletion of tasks with confirmation
- **FR-011**: System MUST persist all task data across sessions
- **FR-012**: System MUST prevent users from accessing or modifying other users' tasks
- **FR-013**: System MUST provide logout functionality that terminates the session
- **FR-014**: System MUST redirect unauthenticated users to login when accessing protected routes
- **FR-015**: System MUST provide a responsive interface usable on desktop and mobile devices

### Key Entities

- **User**: Represents a registered user with unique email, hashed password, name, and timestamps. Each user owns zero or more tasks.
- **Task**: Represents a to-do item with title, optional description, completion status, and timestamps. Each task belongs to exactly one user.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete registration in under 1 minute
- **SC-002**: Users can log in and see their tasks in under 5 seconds
- **SC-003**: Task creation, update, and deletion operations complete in under 2 seconds
- **SC-004**: 95% of users can complete their first task creation without assistance
- **SC-005**: System supports at least 100 concurrent authenticated users
- **SC-006**: Users can access and use the application on mobile devices without horizontal scrolling
- **SC-007**: All user data remains private and isolated - no user can ever see another user's tasks
- **SC-008**: Session remains valid for at least 7 days of inactivity

## Assumptions

- Users have access to a modern web browser (Chrome, Firefox, Safari, Edge - last 2 versions)
- Users have a valid email address for registration
- Network connectivity is generally reliable (offline mode not required for MVP)
- Single language support (English) is sufficient for initial release
- Password reset functionality can be added in a future iteration (not MVP)
- Social login (Google, GitHub) is not required for MVP

## Out of Scope

- Task categories, tags, or labels
- Task due dates and reminders
- Task sharing or collaboration between users
- Bulk task operations
- Task search or filtering
- Data export/import functionality
- Email verification during registration
- Two-factor authentication
- Password reset functionality
- Offline support

---

## Phase 2.1: UI/UX Enhancement - Google Keep Style

**Added**: 2025-12-03
**Status**: In Progress
**Goal**: Transform the basic todo interface into a polished Google Keep-inspired UI with dark/light themes, masonry grid, color-coded notes, and smooth animations.

### User Story 9 - Dark/Light Theme Toggle (Priority: P1)

A user wants to switch between dark and light themes based on their preference or environment. They click a toggle in the header and the entire UI updates immediately.

**Why this priority**: Theme support is foundational for the new UI - all components depend on CSS variables.

**Acceptance Scenarios**:

1. **Given** a user on any page, **When** they click the theme toggle, **Then** the UI immediately switches between dark and light mode
2. **Given** a user with system preference for dark mode, **When** they first visit the app, **Then** the app defaults to dark mode
3. **Given** a user who selected a theme, **When** they return later, **Then** their preference is remembered

---

### User Story 10 - Masonry Grid Layout (Priority: P1)

A user with multiple tasks wants to see them displayed in a compact, Pinterest-style masonry grid that efficiently uses screen space.

**Why this priority**: The grid layout is the core visual change and affects all task display.

**Acceptance Scenarios**:

1. **Given** a user with multiple tasks, **When** they view the dashboard, **Then** tasks are displayed in a responsive masonry grid (1-5 columns based on screen width)
2. **Given** a user viewing tasks, **When** they toggle to list view, **Then** tasks display in a single column
3. **Given** a user on mobile, **When** they view tasks, **Then** the grid adjusts to 1-2 columns appropriately

---

### User Story 11 - Color-Coded Tasks (Priority: P2)

A user wants to visually organize their tasks using background colors. They can assign any of 12 colors to a task for categorization.

**Why this priority**: Color coding is a signature Google Keep feature that adds visual organization.

**Acceptance Scenarios**:

1. **Given** a user creating/editing a task, **When** they click the color picker, **Then** they see 12 color options
2. **Given** a user selecting a color, **When** they apply it, **Then** the task card background changes immediately
3. **Given** a user in dark mode, **When** they view colored tasks, **Then** colors are muted appropriately for dark theme

---

### User Story 12 - Expandable Note Input (Priority: P2)

A user wants a streamlined input experience. The "Take a note..." bar expands to reveal title, content, and toolbar when clicked.

**Why this priority**: This Google Keep interaction pattern improves the creation experience.

**Acceptance Scenarios**:

1. **Given** a user on the dashboard, **When** they see the input, **Then** it displays as a single-line "Take a note..." placeholder
2. **Given** a user clicking the input, **When** it expands, **Then** they see title field, content area, and toolbar with color picker
3. **Given** a user with content entered, **When** they click outside, **Then** the task is auto-saved and form collapses

---

### User Story 13 - Pin Tasks to Top (Priority: P3)

A user wants to keep important tasks visible at the top of their list regardless of creation date.

**Why this priority**: Pinning is a useful organization feature but not core to the visual redesign.

**Acceptance Scenarios**:

1. **Given** a user viewing a task, **When** they click the pin icon, **Then** the task moves to a "Pinned" section at the top
2. **Given** a user with pinned tasks, **When** they view the dashboard, **Then** pinned tasks appear above "Others"
3. **Given** a user unpinning a task, **When** they click the pin icon again, **Then** the task moves back to the regular section

---

### User Story 14 - Task Edit Modal (Priority: P3)

A user wants to edit a task in a focused modal view with all editing options available.

**Why this priority**: The modal provides a better editing experience than inline editing.

**Acceptance Scenarios**:

1. **Given** a user viewing tasks, **When** they click a task card, **Then** a modal opens with the full task
2. **Given** a user in the modal, **When** they edit title/content, **Then** changes are saved on close
3. **Given** a user in the modal, **When** they press Escape or click outside, **Then** the modal closes with changes saved

---

### User Story 15 - Left Sidebar Navigation (Priority: P4)

A user wants persistent navigation for future features like Archive and Trash.

**Why this priority**: Sidebar establishes the layout pattern even if some items are placeholders.

**Acceptance Scenarios**:

1. **Given** a user on the dashboard, **When** they view the left side, **Then** they see a sidebar with Notes, Reminders, Archive, Trash icons
2. **Given** a user clicking Notes, **When** the page loads, **Then** Notes is highlighted as active
3. **Given** a user on mobile, **When** they view the app, **Then** the sidebar is collapsible via hamburger menu

---

### Requirements (UI/UX Enhancement)

- **FR-016**: System MUST support dark and light theme with runtime toggle
- **FR-017**: System MUST persist theme preference in localStorage
- **FR-018**: System MUST display tasks in responsive masonry grid (1-5 columns)
- **FR-019**: System MUST support grid/list view toggle
- **FR-020**: System MUST allow 12 background colors for tasks
- **FR-021**: System MUST store task color in database
- **FR-022**: System MUST display expandable "Take a note..." input
- **FR-023**: System MUST support pinning tasks to top of list
- **FR-024**: System MUST store pinned status in database
- **FR-025**: System MUST open task edit modal on card click
- **FR-026**: System MUST display left sidebar navigation
- **FR-027**: System MUST use Framer Motion for animations (cards, modal, sidebar)

### Success Criteria (UI/UX Enhancement)

- **SC-009**: Theme toggle updates UI in under 100ms
- **SC-010**: Cards animate smoothly on add/remove (60fps)
- **SC-011**: Modal opens/closes with scale animation
- **SC-012**: Grid reflows responsively on window resize
- **SC-013**: All interactive elements have hover/focus states
- **SC-014**: Dark mode colors pass WCAG AA contrast requirements

---

## Phase 2.2: Advanced Features - Trash, Archive, Labels & Reminders

**Added**: 2025-12-03
**Status**: Completed
**Goal**: Add Google Keep-inspired organization features including soft delete, archiving, labels, and reminders.

### User Story 16 - Trash (Soft Delete) (Priority: P1)

A user wants to safely delete tasks without permanent data loss. When they delete a task, it moves to Trash where they can restore it or permanently delete it.

**Why this priority**: Soft delete prevents accidental data loss and is a core safety feature.

**Acceptance Scenarios**:

1. **Given** a user viewing a task, **When** they click delete, **Then** the task moves to Trash (not permanently deleted)
2. **Given** a user on `/dashboard/trash`, **When** they view trashed tasks, **Then** they see all their trashed items with restore/delete options
3. **Given** a user viewing a trashed task, **When** they click "Restore", **Then** the task returns to their main notes
4. **Given** a user viewing a trashed task, **When** they click "Delete forever", **Then** the task is permanently removed
5. **Given** a user on the Trash page, **When** they click "Empty Trash", **Then** all trashed tasks are permanently deleted
6. **Given** a user on the Trash page, **When** they view the page, **Then** they see a warning banner "Notes in Trash are deleted after 7 days"

---

### User Story 17 - Archive (Priority: P2)

A user wants to declutter their main notes view by archiving completed or inactive tasks while keeping them accessible.

**Why this priority**: Archive helps users organize without losing data.

**Acceptance Scenarios**:

1. **Given** a user viewing a task card, **When** they click the Archive icon, **Then** the task moves to Archive
2. **Given** a user on `/dashboard/archive`, **When** they view archived tasks, **Then** they see all their archived items
3. **Given** a user viewing an archived task, **When** they click "Unarchive", **Then** the task returns to the main notes view
4. **Given** a user on the main dashboard, **When** they view their tasks, **Then** archived tasks are not shown

---

### User Story 18 - Labels (Priority: P2)

A user wants to categorize their tasks with custom labels for better organization and filtering.

**Why this priority**: Labels provide flexible organization for users with many tasks.

**Acceptance Scenarios**:

1. **Given** a user clicking "Edit labels" in the sidebar, **When** the modal opens, **Then** they can create, edit, and delete labels
2. **Given** a user with labels, **When** they view the sidebar, **Then** their labels appear dynamically
3. **Given** a user clicking a label in the sidebar, **When** the page loads, **Then** they see tasks filtered by that label at `/dashboard/labels/[id]`
4. **Given** a user editing a task, **When** they assign labels, **Then** the task can have multiple labels (many-to-many)
5. **Given** a user deleting a label, **When** they confirm, **Then** the label is removed but associated tasks are NOT deleted

---

### User Story 19 - Reminders (Priority: P3)

A user wants to set date/time reminders on tasks to be notified or track when items are due.

**Why this priority**: Reminders add time-based organization to tasks.

**Acceptance Scenarios**:

1. **Given** a user viewing a task card, **When** they click the reminder bell icon, **Then** a Google Keep-style picker opens
2. **Given** a user in the reminder picker, **When** they see preset options, **Then** they can choose "Today 8:00 PM", "Tomorrow 8:00 AM", or "Next week Monday 8:00 AM"
3. **Given** a user in the reminder picker, **When** they click "Pick date & time", **Then** they can select a custom date and time
4. **Given** a task with a reminder, **When** displayed on a card, **Then** a reminder chip shows the formatted date/time
5. **Given** a user on `/dashboard/reminders`, **When** they view the page, **Then** tasks are grouped into "SENT" (past) and "UPCOMING" (future) sections
6. **Given** a user with an existing reminder, **When** they open the picker, **Then** they can click "Remove reminder" to clear it

---

### Requirements (Phase 2.2)

- **FR-028**: System MUST implement soft delete using `deleted_at` timestamp
- **FR-029**: System MUST provide `/dashboard/trash` route showing trashed items
- **FR-030**: System MUST allow restore and permanent delete of trashed items
- **FR-031**: System MUST display 7-day trash warning (display only, no auto-delete)
- **FR-032**: System MUST provide "Empty Trash" functionality
- **FR-033**: System MUST allow archiving tasks with `archived` boolean field
- **FR-034**: System MUST provide `/dashboard/archive` route showing archived items
- **FR-035**: System MUST allow unarchiving tasks back to main view
- **FR-036**: System MUST support Label entity with CRUD operations
- **FR-037**: System MUST support many-to-many task-label relationship via junction table
- **FR-038**: System MUST display labels dynamically in sidebar
- **FR-039**: System MUST provide `/dashboard/labels/[id]` route for filtering by label
- **FR-040**: System MUST support `reminder_at` datetime field on tasks
- **FR-041**: System MUST provide Google Keep-style reminder picker with presets
- **FR-042**: System MUST display reminder chips on task cards
- **FR-043**: System MUST provide `/dashboard/reminders` route with SENT/UPCOMING sections

### Success Criteria (Phase 2.2)

- **SC-015**: Soft delete moves task to trash instantly (under 500ms)
- **SC-016**: Restore and permanent delete complete in under 1 second
- **SC-017**: Label CRUD operations complete in under 1 second
- **SC-018**: Reminder picker displays preset options correctly based on current time
- **SC-019**: All 4 routes (/trash, /archive, /reminders, /labels/[id]) load correctly

---

## Phase 2.3: Image Upload with Cloudflare R2

**Added**: 2025-12-03
**Status**: In Progress
**Goal**: Enable users to attach images to their notes using Cloudflare R2 storage.

### User Story 20 - Upload Image to Note (Priority: P1)

A user wants to add images to their notes for visual context. They click the image button, select a file, and the image uploads and displays on the note.

**Why this priority**: Core functionality - users need to upload before viewing.

**Acceptance Scenarios**:

1. **Given** a user editing a note, **When** they click "Add image", **Then** a file picker opens for image selection
2. **Given** a user selecting an image, **When** the file is valid (JPEG, PNG, GIF, WebP under 5MB), **Then** it uploads and appears on the note
3. **Given** a user selecting an invalid file, **When** it exceeds 5MB or wrong type, **Then** an error message displays
4. **Given** a user with a note, **When** they view it, **Then** they see all attached images as thumbnails

---

### User Story 21 - View Image in Full Size (Priority: P2)

A user wants to see an attached image in full size. They click a thumbnail and a modal opens with the full image.

**Why this priority**: Viewing enhances the value of uploaded images.

**Acceptance Scenarios**:

1. **Given** a user viewing a note with images, **When** they click a thumbnail, **Then** a full-size viewer modal opens
2. **Given** a user in the image viewer, **When** they press Escape or click outside, **Then** the modal closes
3. **Given** multiple images on a note, **When** the viewer is open, **Then** they can navigate between images

---

### User Story 22 - Delete Image from Note (Priority: P2)

A user wants to remove an image they no longer need. They can delete images from their notes.

**Why this priority**: Users need control over their content.

**Acceptance Scenarios**:

1. **Given** a user viewing a note with images, **When** they hover over an image, **Then** a delete button appears
2. **Given** a user clicking delete on an image, **When** they confirm, **Then** the image is removed from the note
3. **Given** a deleted image, **When** the operation completes, **Then** it's permanently removed from storage

---

### Requirements (Phase 2.3)

- **FR-044**: System MUST allow image upload via POST `/api/tasks/{id}/images` (multipart/form-data)
- **FR-045**: System MUST validate image type (JPEG, PNG, GIF, WebP only)
- **FR-046**: System MUST enforce max file size of 5MB per image
- **FR-047**: System MUST enforce max 10 images per task
- **FR-048**: System MUST store images in Cloudflare R2 with unique keys
- **FR-049**: System MUST return public URLs for uploaded images
- **FR-050**: System MUST allow listing images for a task via GET `/api/tasks/{id}/images`
- **FR-051**: System MUST allow deleting images via DELETE `/api/images/{id}`
- **FR-052**: System MUST delete from R2 storage when image record is deleted
- **FR-053**: System MUST display image thumbnails on task cards
- **FR-054**: System MUST provide full-size image viewer modal

### Success Criteria (Phase 2.3)

- **SC-020**: Image upload completes in under 5 seconds for 5MB file
- **SC-021**: Thumbnails load within 1 second after task card renders
- **SC-022**: Full-size viewer opens in under 500ms
- **SC-023**: Invalid file types/sizes show error immediately (no upload attempt)
