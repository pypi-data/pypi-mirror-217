UPDATE swoop.action SET parent_uuid = NULL WHERE action_type = 'workflow';

ALTER TABLE swoop.action
DROP CONSTRAINT workflow_or_callback,
ADD CONSTRAINT workflow_or_callback CHECK (
  CASE
    WHEN action_type = 'callback'
      THEN
        parent_uuid IS NOT NULL
        AND payload_uuid IS NULL
    WHEN action_type = 'workflow' THEN
      action_name IS NOT NULL
      AND payload_uuid IS NOT NULL
      AND parent_uuid IS NULL
  END
);
