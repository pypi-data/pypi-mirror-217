import { JupyterFrontEnd } from '@jupyterlab/application';
import { AiService } from './handler';
import { Widget } from '@lumino/widgets';

export type InsertionContext = {
  widget: Widget;
  request: AiService.IPromptRequest;
  response: AiService.IPromptResponse;
};

/**
 * Function that handles the insertion of Prompt API output into the
 * active document. This function expects that a command with an id
 * of `ai:insert-<insertion-mode>` is registered, context is passed
 * through to the command for handling insertion. See `InsertionContext`
 * for more info.
 *
 * @param app - Jupyter front end application
 * @param context - Insertion context
 */
export async function insertOutput(
  app: JupyterFrontEnd,
  context: InsertionContext
): Promise<boolean> {
  app.commands.execute(
    `ai:insert-${context.response.insertion_mode}`,
    context as any
  );
  return true;
}
