import { pipeline, env } from "@xenova/transformers";

// Skip remote check and use local models if available
env.allowRemoteModels = true; // Set to true for initial download, but can be configured for offline
env.localModelPath = './models/';

class MyClassificationPipeline {
  static task = 'text2text-generation';
  static model = 'Xenova/LaMini-Flan-T5-78M';
  static instance = null;

  static async getInstance(progress_callback = null) {
    if (this.instance === null) {
      this.instance = pipeline(this.task, this.model, { progress_callback });
    }
    return this.instance;
  }
}

// Listen for messages from the main thread
self.addEventListener('message', async (event) => {
  const { text, type } = event.data;

  if (type === 'generate') {
    try {
      const generator = await MyClassificationPipeline.getInstance((x) => {
        // Send progress updates back to the main thread
        self.postMessage({
          status: 'progress',
          ...x
        });
      });

      const output = await generator(text, {
        max_new_tokens: 256,
        temperature: 0.7,
        do_sample: true,
        callback_function: (beams) => {
            const decodedText = generator.tokenizer.decode(beams[0].output_token_ids, {
                skip_special_tokens: true,
            });
            self.postMessage({
                status: 'update',
                output: decodedText
            });
        }
      });

      self.postMessage({
        status: 'complete',
        output: output[0].generated_text
      });
    } catch (error) {
      self.postMessage({
        status: 'error',
        error: error.message
      });
    }
  }
});
